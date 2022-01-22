from app.core.entities.game_session import GameSessionEntity
from app.routing.callbacks import CallbackIds
from base.api.handler import Context, InlineMenu, InlineMenuButton


class GameRankingHandlers:
    @staticmethod
    def build_main_menu(context: Context):
        menu = list()
        existing_session = GameSessionEntity.get(context)
        if existing_session is not None:
            menu.append([InlineMenuButton('Start new match!', CallbackIds.TS_MATCH_MENU)])
            menu.append([InlineMenuButton('Manage session...', CallbackIds.TS_SESSION_MENU, existing_session.id),
                         InlineMenuButton('Stop session', CallbackIds.TS_STOP_SESSION, existing_session.id)])
        menu.append([InlineMenuButton('New game session...', CallbackIds.TS_NEW_SESSION)])
        menu.append([InlineMenuButton('Manage players...', CallbackIds.TS_PLAYERS_MENU)])
        menu.append([InlineMenuButton('Close', CallbackIds.COMMON_DELETE_MESSAGE)])
        return InlineMenu(menu, context.sender.tg_id)

    @staticmethod
    def main_menu(context: Context):
        context.actions.send_message('Game Rankings', reply_markup=GameRankingHandlers.build_main_menu(context))

    @staticmethod
    def main_menu_callback(context: Context):
        context.actions.edit_markup(GameRankingHandlers.build_main_menu(context))

    @staticmethod
    def stop_session(context: Context):
        GameSessionEntity.stop_current_session(context)
        GameRankingHandlers.main_menu_callback(context)
