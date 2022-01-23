from typing import List

from app.core.entities.game_ranking import GameRankingEntity
from app.core.entities.game_session import GameSessionEntity
from app.models.all import Player
from base.api.handler import Context


class PlayerEntity:
    @staticmethod
    def get_for_ranking(context: Context) -> List[Player]:
        game_ranking = GameRankingEntity.get_or_create(context)
        return context.session.query(Player).filter(Player.game_ranking_id == game_ranking.id).all()

    @staticmethod
    def get_for_session(context: Context):
        current_session = GameSessionEntity.get(context)
        return context.session.query(Player).filter(Player.game_session_id == current_session.id).all()

    @staticmethod
    def get_id_map_for_session(context: Context):
        players = PlayerEntity.get_for_session(context)
        return {player.id: player for player in players}
