from app.api.command_list import CallbackId
from app.core.game_session import GameSessionHelpers
from app.core.player import PlayerHelpers
from app.models.all import Player
from base.api.handler import Context, InlineMenu, InlineMenuButton


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
        context.actions.edit_message(GameSessionHelpers.text_description(context))
        context.actions.edit_markup(GameSessionHandlers._build_menu_markup(context))

    @staticmethod
    def create_new(context: Context):
        GameSessionHelpers.stop_current_session(context)
        # After previous step, new session will be created.
        GameSessionHelpers.get_or_create(context)
        GameSessionHandlers.open_menu(context)

    @staticmethod
    def choose_player(context: Context):
        player_id = context.data.callback_data.data
        player = context.session.query(Player).filter(Player.id == player_id).one_or_none()
        if player is not None:
            game_session = GameSessionHelpers.get_or_create(context)
            if player.game_session_id == game_session.id:
                player.game_session_id = None
            else:
                player.game_session_id = game_session.id
            context.session.commit()
        GameSessionHandlers.open_menu(context)
