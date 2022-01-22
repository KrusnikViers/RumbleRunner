from trueskill import TrueSkill

DEFAULT_MU = 100  # Initial estimation
DEFAULT_SIGMA = 33  # Initial deviation
_BETA = DEFAULT_SIGMA  # Skill distance (Distance between MU-values that marks 80% chance of winning)
_TAU = DEFAULT_SIGMA / 10.0  # Dynamic factor, defines volatility of skill estimations


class TSClient:
    trueskill = TrueSkill(mu=DEFAULT_MU, sigma=DEFAULT_SIGMA, beta=_BETA, tau=_TAU, draw_probability=0.0)
