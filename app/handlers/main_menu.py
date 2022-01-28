from app import PROJECT_FULL_NAME
from app.api import CallbackId
from app.core import GameSessionHelpers
from app.core.player import PlayerHelpers
from base import Context, InlineMenu, InlineMenuButton


class MainMenuHandlers:
    @staticmethod
    def _markup(context: Context) -> InlineMenu:
        menu = list()
        if GameSessionHelpers.get(context) is not None:
            if len(PlayerHelpers.get_for_session(context)) >= 2:
                menu.append([InlineMenuButton('Start new match', CallbackId.MATCHUP_SELECTION_OPEN)])
            menu.append([InlineMenuButton('Change participants', CallbackId.SESSION_PLAYERS_OPEN)])
            menu.append([InlineMenuButton('Stop session', CallbackId.MAIN_MENU_STOP_SESSION)])
        else:
            menu.append([InlineMenuButton('Start game session', CallbackId.SESSION_PLAYERS_NEW)])
        menu.append([InlineMenuButton('Players list', CallbackId.PLAYERS_LIST_OPEN)])
        menu.append([InlineMenuButton('Close menu', CallbackId.COMMON_DELETE_MESSAGE)])
        return context.personal_menu(menu)

    @staticmethod
    def _title(context: Context) -> str:
        return "{}\n\n".format(PROJECT_FULL_NAME) + GameSessionHelpers.text_description(context)

    @staticmethod
    def open(context: Context):
        if context.message.is_callback:
            context.delete_message()
        context.send_message(text=MainMenuHandlers._title(context), reply_markup=MainMenuHandlers._markup(context))

    @staticmethod
    def redraw(context: Context):
        context.edit_message(MainMenuHandlers._title(context), reply_markup=MainMenuHandlers._markup(context))

    @staticmethod
    def stop_session(context: Context):
        GameSessionHelpers.stop_current_session(context)
        MainMenuHandlers.open(context)
