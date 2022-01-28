from typing import List

from app.core.game_ranking import GameRankingHelpers
from app.core.game_session import GameSessionHelpers
from app.models import Player
from base import SessionScope, Context


class PlayerHelpers:
    @staticmethod
    def get_for_ranking(context: Context) -> List[Player]:
        game_ranking = GameRankingHelpers.get_or_create(context)
        return SessionScope.session().query(Player).filter(Player.game_ranking_id == game_ranking.id).all()

    @staticmethod
    def get_for_session(context: Context):
        current_session = GameSessionHelpers.get(context)
        return SessionScope.session().query(Player).filter(Player.game_session_id == current_session.id).all()

    @staticmethod
    def get_id_map_for_session(context: Context):
        players = PlayerHelpers.get_for_session(context)
        return {player.id: player for player in players}
