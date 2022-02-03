import logging

from app.core.trueskill import TrueSkillParams, TrueSkillPlayer, TrueSkillMatchup, TrueSkillClient
from app.models import Player, GameRanking
from base import SessionScope
from tests.utils import InBotTestCase


class TestMatch:
    def __init__(self, winners: list, lost: list):
        self.winners = winners
        self.lost = lost


HISTORICAL = [
    TestMatch([1, 2, 3], [4, 5, 6]),
    TestMatch([4, 1, 2], [3, 6, 5]),
    TestMatch([3, 2, 5], [4, 7, 8]),
    TestMatch([3, 5, 7], [4, 2, 8]),
    TestMatch([4, 8, 3], [2, 5, 9, 7]),
    TestMatch([3, 7, 5], [4, 6, 1]),
    TestMatch([3, 1, 6], [4, 5, 7]),
    TestMatch([3, 1, 6], [4, 5, 7]),
    TestMatch([3, 7, 1], [4, 6, 5]),
    TestMatch([3, 5, 6], [4, 8, 9]),
    TestMatch([4, 8, 9], [6, 7, 3]),
    TestMatch([1, 3, 2], [4, 6, 5]),
    TestMatch([4, 8, 3], [2, 5, 9, 7]),
    TestMatch([4, 8, 9], [6, 7, 3]),
    TestMatch([3, 5, 6], [4, 8, 9]),
    TestMatch([4, 9, 2], [3, 1, 8, 5]),
    TestMatch([3, 9], [4, 2]),
    TestMatch([3, 4, 9], [8, 5, 1]),
    TestMatch([4, 3, 2], [9, 1, 5]),
    TestMatch([3, 1, 2], [9, 5, 4]),
    TestMatch([2, 9, 1], [4, 3, 5]),
    TestMatch([8, 4, 5, 7], [3, 6, 1]),
    TestMatch([4, 3, 7], [8, 5, 1, 6]),
    TestMatch([5, 0, 3, 6], [7, 4, 9, 2]),
    TestMatch([2, 3, 6, 5], [4, 7, 9, 0]),
    TestMatch([2, 0, 6, 5], [3, 4, 7, 9]),
    TestMatch([4, 0, 9], [5, 7, 6]),
    TestMatch([5, 7, 0], [9, 6, 4]),
    TestMatch([3, 5], [6, 4]),
    TestMatch([4, 3], [6, 5]),
    TestMatch([4, 1, 7, 6], [3, 2, 8]),
    TestMatch([3, 6, 7], [4, 1, 2]),
    TestMatch([4, 3, 1], [6, 2, 7]),
    TestMatch([3, 6, 1], [4, 2, 7]),
    TestMatch([4, 3, 7], [1, 6, 2]),
    TestMatch([3, 0, 5], [7, 1, 4, 2]),
    TestMatch([3, 1, 7], [4, 5, 2]),
    TestMatch([3, 7, 2, 8], [0, 4, 1, 5]),
    TestMatch([0, 4, 5], [7, 1, 2]),
    TestMatch([0, 7, 5, 2], [4, 1, 8, 3]),
    TestMatch([4, 7, 8, 3], [0, 1, 5, 2]),
    TestMatch([4, 1, 6, 3], [0, 7, 5, 2]),
    TestMatch([4, 6, 2], [7, 9, 3, 0]),
    TestMatch([6, 3, 5, 9], [4, 2, 0, 7]),
    TestMatch([6, 2, 7, 0], [4, 9, 3, 5]),
    TestMatch([4, 2, 5, 0], [6, 9, 7, 3]),
    TestMatch([6, 2, 9], [4, 7, 8]),
]


def r_(number):
    return round(number, 2)


class TestHistorical(InBotTestCase):
    def test(self):
        players = {}
        # logging.disable(logging.NOTSET)
        logging.getLogger().setLevel(logging.INFO)
        with SessionScope(self.connection) as session:
            session.add(GameRanking(id=1, tg_group_id=1))
            for i in range(0, 10):
                players[i] = Player(id=i, name='Player {}'.format(i), game_ranking_id=1,
                                    mu=TrueSkillParams.DEFAULT_MU, sigma=TrueSkillParams.DEFAULT_SIGMA)
                session.add(players[i])
            guessed = 0
            total = 0
            for match in HISTORICAL:
                matchup = TrueSkillMatchup(
                    [TrueSkillPlayer(players[index]) for index in match.winners],
                    [TrueSkillPlayer(players[index]) for index in match.lost]
                )
                logging.info('Match {}vs{} : Quality {} : Chance {}'.format(
                    len(match.winners), len(match.lost), r_(matchup.uncertainty), r_(matchup.win_chance)))
                if matchup.win_chance >= 0.5:
                    guessed += 1
                total += 1

                TrueSkillClient.update_players(
                    [players[index] for index in match.winners],
                    [players[index] for index in match.lost]
                )
            for i, player in players.items():
                logging.info('{} : {}:{}'.format(
                    player.name, r_(player.mu), r_(player.sigma)))
            logging.info('Guessing: {}'.format(r_(guessed / total)))
            self.assertGreater(guessed / total, 0.5)
