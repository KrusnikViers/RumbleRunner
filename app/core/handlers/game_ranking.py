from app.api.command_list import CallbackId
from app.core.entities.game_ranking import GameRankingEntity
from app.core.entities.game_session import GameSessionEntity
from app.core.entities.player import PlayerEntity
from base.api.handler import Context, InlineMenu, InlineMenuButton


class GameRankingHandlers:
    @staticmethod
    def build_main_menu(context: Context):
        menu = list()
        existing_session = GameSessionEntity.get(context)
        if existing_session is not None:
            menu.append([InlineMenuButton('Start new match!', CallbackId.TS_MATCH_MENU)])
            menu.append([InlineMenuButton('Edit session..', CallbackId.TS_SESSION_MENU, existing_session.id),
                         InlineMenuButton('Stop session', CallbackId.TS_STOP_SESSION, existing_session.id)])
        menu.append([InlineMenuButton('Start new session..', CallbackId.TS_NEW_SESSION)])
        menu.append([InlineMenuButton('Change players..', CallbackId.TS_PLAYERS_MENU)])
        menu.append([InlineMenuButton('Close menu', CallbackId.COMMON_DELETE_MESSAGE)])
        return InlineMenu(menu, context.sender.tg_id)

    @staticmethod
    def main_menu_title(context: Context) -> str:
        message = 'Let\'s rumble!'
        ranking = GameRankingEntity.get_or_create(context)
        message += '\n\n' + GameSessionEntity.text_description(context)
        return message

    @staticmethod
    def main_menu(context: Context):
        context.actions.send_message(GameRankingHandlers.main_menu_title(context),
                                     reply_markup=GameRankingHandlers.build_main_menu(context))

    @staticmethod
    def main_menu_callback(context: Context):
        context.actions.edit_message(GameRankingHandlers.main_menu_title(context))
        context.actions.edit_markup(GameRankingHandlers.build_main_menu(context))

    @staticmethod
    def stop_session(context: Context):
        GameSessionEntity.stop_current_session(context)
        GameRankingHandlers.main_menu_callback(context)
