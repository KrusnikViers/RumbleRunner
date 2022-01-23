from itertools import combinations
from math import sqrt
from typing import List

import trueskill

from app.core.player import PlayerHelpers
from app.models.all import Player
from base.api.handler import Context


class TrueSkillParams:
    DEFAULT_MU = 25  # Initial estimation
    DEFAULT_SIGMA = DEFAULT_MU / 3  # Initial deviation
    BETA = DEFAULT_SIGMA / 2.0  # Skill distance (Distance between MU-values that marks 80% chance of winning)
    TAU = DEFAULT_SIGMA / 100.0  # Dynamic factor, defines volatility of skill estimations
    DRAW_PROBABILITY = 0.0


_ts_instance = trueskill.TrueSkill(mu=TrueSkillParams.DEFAULT_MU, sigma=TrueSkillParams.DEFAULT_SIGMA,
                                   beta=TrueSkillParams.BETA, tau=TrueSkillParams.TAU,
                                   draw_probability=TrueSkillParams.DRAW_PROBABILITY)


class TrueSkillPlayer:
    def __init__(self, player: Player):
        self.id = player.id
        self.rating = trueskill.Rating(player.mu, player.sigma)
        self.winrate_diff = TrueSkillPlayer._calculate_winrate_diff(player)

    def __lt__(self, other):
        return (self.id < other.id) if self.rating.sigma == other.rating.sigma else (
                self.rating.sigma < other.rating.sigma)

    @staticmethod
    def _calculate_winrate_diff(player: Player) -> float:
        last_participations = player.participations[:10]
        if not len(last_participations):
            return 0
        winrate = sum(1 if p.is_winner else 0 for p in last_participations) / len(last_participations)
        return max(0.0, 0.4 - winrate) ** 2


class TrueSkillMatchup:
    def __init__(self, team_1: List[TrueSkillPlayer], team_2: List[TrueSkillPlayer]):
        self.team_1 = sorted(team_1)
        self.team_2 = sorted(team_2)
        self.quality = self._calculate_quality()
        self.win_chance = self._get_win_chance()
        self.satisfaction = self._get_satisfaction()

    def _calculate_quality(self) -> float:
        return _ts_instance.quality([
            tuple(player.rating for player in self.team_1), tuple(player.rating for player in self.team_2)
        ])

    def _get_win_chance(self):
        delta_mu = sum(player.rating.mu for player in self.team_1) - sum(player.rating.mu for player in self.team_2)
        sum_sigma_squared = sum(player.rating.sigma ** 2 for player in (self.team_1 + self.team_2))
        denominator = sqrt(
            (len(self.team_1) + len(self.team_2)) * (TrueSkillParams.BETA * TrueSkillParams.BETA) + sum_sigma_squared
        )
        return _ts_instance.cdf(delta_mu / denominator)

    def _get_satisfaction(self) -> float:
        favourites, outsiders = (self.team_1, self.team_2) if self.win_chance > 0.5 else (self.team_2, self.team_1)
        if self.win_chance > 0.6 or self.win_chance < 0.4:
            return sum(player.winrate_diff for player in favourites) - sum(player.winrate_diff for player in outsiders)
        return 0


class TrueSkillClient:
    @staticmethod
    def _signature(team: List[TrueSkillPlayer]):
        return ':'.join(sorted([str(ts_player.id) for ts_player in team]))

    @staticmethod
    def calculate_matchups(context: Context) -> List[TrueSkillMatchup]:
        players = PlayerHelpers.get_for_session(context)
        assert len(players) > 2
        ts_players = [TrueSkillPlayer(player) for player in players]

        matchups = []
        checked = set()
        for team_size in range(1, len(ts_players) // 2 + 1):
            for combination in combinations(ts_players, team_size):
                team_1 = combination
                team_2 = [player for player in ts_players if player not in team_1]
                if TrueSkillClient._signature(team_1) in checked or TrueSkillClient._signature(team_2) in checked:
                    continue
                checked.add(TrueSkillClient._signature(team_1))
                matchups.append(TrueSkillMatchup(team_1, team_2))
        return sorted(matchups, key=lambda x: x.quality, reverse=True)

    @staticmethod
    def update_players(team_won: List[Player], team_lost: List[Player]):
        ratings_won, ratings_lost = _ts_instance.rate([
            [trueskill.Rating(player.mu, player.sigma) for player in team_won],
            [trueskill.Rating(player.mu, player.sigma) for player in team_lost]
        ])
        for new_rating, player in zip((ratings_won + ratings_lost), (team_won + team_lost)):
            player.mu = new_rating.mu
            player.sigma = new_rating.sigma
