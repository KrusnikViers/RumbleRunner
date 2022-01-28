from sqlalchemy import and_

from app.core.game_ranking import GameRankingHelpers
from app.models.all import GameSession, Player
from base.api.database import SessionScope
from base.api.handler import Context


class GameSessionHelpers:
    @staticmethod
    def get(context: Context) -> GameSession:
        ranking = GameRankingHelpers.get_or_create(context)
        return SessionScope.session().query(GameSession).filter(and_(
            GameSession.is_ongoing == True,
            GameSession.game_ranking_id == ranking.id)).one_or_none()

    @staticmethod
    def get_or_create(context: Context):
        game_session = GameSessionHelpers.get(context)
        if game_session is None:
            ranking = GameRankingHelpers.get_or_create(context)
            game_session = GameSession(is_ongoing=True, game_ranking_id=ranking.id)
            SessionScope.session().add(game_session)
            SessionScope.commit()
        return game_session

    @staticmethod
    def stop_current_session(context: Context):
        current_session = GameSessionHelpers.get(context)
        if current_session is not None:
            for player in SessionScope.session().query(Player).filter(Player.game_session_id == current_session.id):
                player.game_session_id = None
            current_session.is_ongoing = False
            SessionScope.commit()

    @staticmethod
    def text_description(context: Context):
        current_session = GameSessionHelpers.get(context)
        if not current_session:
            return 'All is quiet for now'
        return 'Game session is in progress!\n\nMatches played: {}\nParticipants: {}'.format(
            current_session.matches_played,
            ', '.join([player.name for player in current_session.players])
        )
