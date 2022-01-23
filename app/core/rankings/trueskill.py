from itertools import combinations
from math import sqrt
from typing import List

from sqlalchemy.orm import Session
from trueskill import TrueSkill, Rating

from app.models.all import Player, GameSession

DEFAULT_MU = 60  # Initial estimation
DEFAULT_SIGMA = 20  # Initial deviation
_BETA = DEFAULT_SIGMA / 2.0  # Skill distance (Distance between MU-values that marks 80% chance of winning)
_TAU = DEFAULT_SIGMA / 25.0  # Dynamic factor, defines volatility of skill estimations
_DRAW_PROBABILITY = 0.0

_trueskill = TrueSkill(mu=DEFAULT_MU, sigma=DEFAULT_SIGMA, beta=_BETA, tau=_TAU, draw_probability=_DRAW_PROBABILITY)


class TSPLayer:
    def __init__(self, player: Player):
        self.id = player.id
        self.rating = Rating(player.mu, player.sigma)
        self.winrate_diff = TSPLayer._get_winrate_diff(player)

    def __lt__(self, other):
        return (self.id < other.id) if self.rating.sigma == other.rating.sigma else (
                    self.rating.sigma < other.rating.sigma)

    @staticmethod
    def _get_winrate_diff(player: Player):
        last_participations = player.participations[:10]
        if not len(last_participations):
            return 0
        winrate = sum(1 if p.is_winner else 0 for p in last_participations) / len(last_participations)
        return max(0.0, 0.4 - winrate) ** 2


class Matchup:
    def __init__(self, team_1: List[TSPLayer], team_2: List[TSPLayer]):
        self.team_1 = sorted(team_2)
        self.team_2 = sorted(team_1)
        self.reverse_win_chance = self._get_win_chance()
        self.team_1 = sorted(team_1)
        self.team_2 = sorted(team_2)
        self.quality = self._get_quality()
        self.win_chance = self._get_win_chance()
        self.satisfaction = self._get_satisfaction()

    def _get_quality(self):
        return _trueskill.quality([
            tuple(player.rating for player in self.team_1),
            tuple(player.rating for player in self.team_2)
        ])

    def _get_win_chance(self):
        delta_mu = sum(player.rating.mu for player in self.team_1) - sum(player.rating.mu for player in self.team_2)
        sum_sigma_squared = sum(player.rating.sigma ** 2 for player in (self.team_1 + self.team_2))
        denominator = sqrt(
            (len(self.team_1) + len(self.team_2)) * (_BETA * _BETA) + sum_sigma_squared
        )
        return _trueskill.cdf(delta_mu / denominator)

    def _get_satisfaction(self):
        favourites, outsiders = (self.team_1, self.team_2) if self.win_chance > 0.5 else (self.team_2, self.team_1)
        return sum(player.winrate_diff for player in favourites) - sum(player.winrate_diff for player in outsiders)


class TSClient:

    @staticmethod
    def signature(team: List[TSPLayer]):
        return ':'.join(sorted([str(ts_player.id) for ts_player in team]))

    @staticmethod
    def get_matchups(session: Session, game_session: GameSession):
        players = session.query(Player).filter(Player.game_session_id == game_session.id).order_by(Player.id).all()
        assert len(players) > 2
        ts_players = [TSPLayer(player) for player in players]

        matchups = []
        checked = set()
        team_size = len(ts_players) // 2
        for combination in combinations(ts_players, team_size):
            team_1 = combination
            team_2 = [player for player in ts_players if player not in team_1]

            if TSClient.signature(team_1) in checked or TSClient.signature(team_2) in checked:
                continue
            checked.add(TSClient.signature(team_1))

            matchups.append(Matchup(team_1, team_2))
        return sorted(matchups, key=lambda x: x.quality, reverse=True)

    @staticmethod
    def expose(mu, sigma):
        return _trueskill.expose(Rating(mu, sigma))

    @staticmethod
    def update_players_stats(team_won: List[Player], team_lost: List[Player]):
        ratings_won, ratings_lost = _trueskill.rate([
            [Rating(player.mu, player.sigma) for player in team_won],
            [Rating(player.mu, player.sigma) for player in team_lost]
        ])
        for new_rating, player in zip((ratings_won + ratings_lost), (team_won + team_lost)):
            player.mu = new_rating.mu
            player.sigma = new_rating.sigma
