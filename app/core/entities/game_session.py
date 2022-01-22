from sqlalchemy import and_

from app.core.entities.game_ranking import GameRankingEntity
from app.models.all import GameSession, Player
from base.api.handler import Context


class GameSessionEntity:
    @staticmethod
    def get(context: Context) -> GameSession:
        ranking = GameRankingEntity.get_or_create(context)
        return context.session.query(GameSession).filter(and_(
            GameSession.is_ongoing == True,
            GameSession.game_ranking_id == ranking.id)).one_or_none()

    @staticmethod
    def get_or_create(context: Context):
        game_session = GameSessionEntity.get(context)
        if game_session is None:
            ranking = GameRankingEntity.get_or_create(context)
            game_session = GameSession(is_ongoing=True, game_ranking_id=ranking.id)
            context.session.add(game_session)
            context.session.commit()
        return game_session

    @staticmethod
    def stop_current_session(context: Context):
        current_session = GameSessionEntity.get(context)
        if current_session is not None:
            for player in context.session.query(Player).filter(Player.game_session_id == current_session.id):
                player.game_session_id = None
            current_session.is_ongoing = False
            context.session.commit()
