from itertools import combinations
from math import sqrt
from typing import List

import trueskill

from app.core.player import PlayerHelpers
from app.models import Player
from base import Context


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
        self.last_results = [p.is_winner for p in sorted(player.participations, key=lambda x: x.id, reverse=True)]

        self.antistreak = self._antistreak()

    def __lt__(self, other):
        return self.id < other.id

    def _antistreak(self):
        if len(self.last_results) < 2:
            return False
        results_to_count = min(len(self.last_results), 6)
        return sum([1 if won else 0 for won in self.last_results[:results_to_count]]) <= (0.4 * results_to_count)


class TrueSkillMatchup:
    def __init__(self, team_1: List[TrueSkillPlayer], team_2: List[TrueSkillPlayer]):
        self.team_1 = sorted(team_1)
        self.team_2 = sorted(team_2)
        self.uncertainty = self._ts_quality()
        self.win_chance = self._win_chance()
        self.streakbreaker = self._streakbreaker()

    def _ts_quality(self) -> float:
        return _ts_instance.quality([
            tuple(player.rating for player in self.team_1), tuple(player.rating for player in self.team_2)
        ])

    def _win_chance(self):
        delta_mu = sum(player.rating.mu for player in self.team_1) - sum(player.rating.mu for player in self.team_2)
        sum_sigma_squared = sum(player.rating.sigma ** 2 for player in (self.team_1 + self.team_2))
        denominator = sqrt(
            (len(self.team_1) + len(self.team_2)) * (TrueSkillParams.BETA * TrueSkillParams.BETA) + sum_sigma_squared
        )
        return _ts_instance.cdf(delta_mu / denominator)

    def _streakbreaker(self) -> float:
        return (0.5 - self.win_chance) * (sum([int(p.antistreak) for p in self.team_2]) -
                                          sum([int(p.antistreak) for p in self.team_1]))


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
        return matchups

    @staticmethod
    def select_good_matchups(context: Context) -> List[TrueSkillMatchup]:
        all_options = TrueSkillClient.calculate_matchups(context)
        most_uncertainty = max([m.uncertainty for m in all_options])
        selection_threshold = 0.2

        good_options = [m for m in all_options if m.uncertainty >= most_uncertainty - selection_threshold]
        return sorted(good_options, key=lambda x: (x.streakbreaker, x.uncertainty), reverse=True)

    @staticmethod
    def update_players(team_won: List[Player], team_lost: List[Player]):
        ratings_won, ratings_lost = _ts_instance.rate([
            [trueskill.Rating(player.mu, player.sigma) for player in team_won],
            [trueskill.Rating(player.mu, player.sigma) for player in team_lost]
        ])
        for new_rating, player in zip((ratings_won + ratings_lost), (team_won + team_lost)):
            player.mu = new_rating.mu
            player.sigma = new_rating.sigma
