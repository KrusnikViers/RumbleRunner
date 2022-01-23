from app.api.command_list import CallbackId
from app.core.game_ranking import GameRankingHelpers
from app.core.game_session import GameSessionHelpers
from base.api.handler import Context, InlineMenu, InlineMenuButton


class GameRankingHandlers:
    @staticmethod
    def _build_menu_markup(context: Context) -> InlineMenu:
        menu = list()
        existing_session = GameSessionHelpers.get(context)
        if existing_session is not None:
            menu.append([InlineMenuButton('Start new match!', CallbackId.TS_MATCH_OPEN_MENU)])
            menu.append([InlineMenuButton('Edit session..',
                                          CallbackId.TS_GAME_SESSION_OPEN_MENU, existing_session.id),
                         InlineMenuButton('Stop session',
                                          CallbackId.TS_RANKING_STOP_GAME_SESSION, existing_session.id)])
        menu.append([InlineMenuButton('Start new session..', CallbackId.TS_GAME_SESSION_CREATE_NEW)])
        menu.append([InlineMenuButton('Manage players..', CallbackId.TS_PLAYERS_MANAGEMENT_OPEN_MENU)])
        menu.append([InlineMenuButton('Close menu', CallbackId.COMMON_DELETE_MESSAGE)])
        return InlineMenu(menu, context.sender.tg_id)

    @staticmethod
    def _build_menu_title(context: Context) -> str:
        message = 'Let\'s rumble!'
        ranking = GameRankingHelpers.get_or_create(context)
        message += '\n\n' + GameSessionHelpers.text_description(context)
        return message

    @staticmethod
    def open_menu(context: Context):
        context.actions.send_message(GameRankingHandlers._build_menu_title(context),
                                     reply_markup=GameRankingHandlers._build_menu_markup(context))

    @staticmethod
    def open_menu_callback(context: Context):
        context.actions.edit_message(GameRankingHandlers._build_menu_title(context))
        context.actions.edit_markup(GameRankingHandlers._build_menu_markup(context))

    @staticmethod
    def stop_game_session(context: Context):
        GameSessionHelpers.stop_current_session(context)
        GameRankingHandlers.open_menu_callback(context)