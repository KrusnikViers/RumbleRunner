from app.api import CallbackId
from app.core import PlayerHelpers, GameSessionHelpers
from app.models import Player
from base import SessionScope, Context, InlineMenu, InlineMenuButton


class GameSessionHandlers:
    @staticmethod
    def _build_menu_markup(context: Context) -> InlineMenu:
        menu = list()
        game_session = GameSessionHelpers.get_or_create(context)
        players = PlayerHelpers.get_for_ranking(context)
        for player in players:
            text_template = '✅ {} (remove)' if player.game_session_id == game_session.id else '⛔ {} (add)'
            menu.append([
                InlineMenuButton(text_template.format(player.name), CallbackId.TS_GAME_SESSION_CHOOSE_PLAYER, player.id)
            ])
        menu.append([InlineMenuButton('Back', CallbackId.TS_RANKING_OPEN_MENU)])
        return InlineMenu(menu, user_tg_id=context.sender.tg_id)

    @staticmethod
    def open_menu(context: Context):
        context.edit_message(GameSessionHelpers.text_description(context))
        context.edit_markup(GameSessionHandlers._build_menu_markup(context))

    @staticmethod
    def create_new(context: Context):
        GameSessionHelpers.stop_current_session(context)
        # After previous step, new session will be created.
        GameSessionHelpers.get_or_create(context)
        GameSessionHandlers.open_menu(context)

    @staticmethod
    def choose_player(context: Context):
        player_id = context.message.data
        player = SessionScope.session().query(Player).filter(Player.id == player_id).one_or_none()
        if player is not None:
            game_session = GameSessionHelpers.get_or_create(context)
            if player.game_session_id == game_session.id:
                player.game_session_id = None
            else:
                player.game_session_id = game_session.id
            SessionScope.commit()
        GameSessionHandlers.open_menu(context)
