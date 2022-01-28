from app.api import CallbackId
from app.core import PlayerHelpers, GameSessionHelpers
from app.models import Player
from base import SessionScope, Context, InlineMenuButton


class SessionPlayersHandlers:
    @staticmethod
    def _title(context: Context):
        return "Choose players who will be participating:"

    @staticmethod
    def _markup(context: Context):
        menu = list()
        game_session = GameSessionHelpers.get_or_create(context)
        players = PlayerHelpers.get_for_ranking(context)
        for player in players:
            text_template = '✅ {}' if player.game_session_id == game_session.id else '{}'
            menu.append([
                InlineMenuButton(text_template.format(player.name), CallbackId.SESSION_PLAYERS_SELECT, player.id)
            ])
        menu.append([InlineMenuButton('Confirm', CallbackId.MAIN_MENU_REDRAW)])
        return context.personal_menu(menu)

    @staticmethod
    def open(context: Context):
        if context.message.is_callback:
            context.delete_message()
        context.send_message(SessionPlayersHandlers._title(context),
                             reply_markup=SessionPlayersHandlers._markup(context))

    @staticmethod
    def redraw(context: Context):
        context.edit_message(SessionPlayersHandlers._title(context),
                             reply_markup=SessionPlayersHandlers._markup(context))

    @staticmethod
    def new(context: Context):
        GameSessionHelpers.stop_current_session(context)
        # After previous step, new session will be created.
        GameSessionHelpers.get_or_create(context)
        SessionPlayersHandlers.redraw(context)

    @staticmethod
    def select(context: Context):
        player_id = context.message.data
        if (player := SessionScope.session().query(Player).filter(Player.id == player_id).one_or_none()) is not None:
            game_session = GameSessionHelpers.get_or_create(context)
            if player.game_session_id == game_session.id:
                player.game_session_id = None
            else:
                player.game_session_id = game_session.id
            SessionScope.commit()
        SessionPlayersHandlers.redraw(context)
