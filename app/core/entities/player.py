from typing import List

from app.models.all import GameRanking, Player
from base.api.handler import Context


class PlayerEntity:
    @staticmethod
    def get_for_ranking(context: Context, game_ranking: GameRanking) -> List[Player]:
        return context.session.query(Player).filter(Player.game_ranking_id == game_ranking.id).all()
