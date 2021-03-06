from sqlalchemy import and_

from app.core.game_ranking import GameRankingHelpers
from app.models import GameSession, Player
from base import SessionScope, Context


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
        if not (current_session := GameSessionHelpers.get(context)):
            return 'No active game session'
        return ("Game session is in progress!\n"
                "Matches played: {}\n"
                "Participants (min 2): {}").format(
            current_session.matches_played,
            ', '.join(sorted([player.name for player in current_session.players]))
        )
