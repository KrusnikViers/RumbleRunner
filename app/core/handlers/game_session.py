from app.api.command_list import CallbackId
from app.core.entities.game_session import GameSessionEntity
from app.core.entities.player import PlayerEntity
from app.models.all import Player
from base.api.handler import Context, InlineMenu, InlineMenuButton


class GameSessionHandlers:
    @staticmethod
    def build_main_menu(context: Context) -> InlineMenu:
        menu = list()
        game_session = GameSessionEntity.get_or_create(context)
        players = PlayerEntity.get_for_ranking(context)
        for player in players:
            text_template = '✅ {} (remove)' if player.game_session_id == game_session.id else '⛔ {} (add)'
            menu.append([
                InlineMenuButton(text_template.format(player.name), CallbackId.TS_CHOOSE_PLAYER_FOR_SESSION, player.id)
            ])
        menu.append([InlineMenuButton('Back', CallbackId.TS_MAIN_MENU)])
        return InlineMenu(menu, user_tg_id=context.sender.tg_id)

    @staticmethod
    def session_menu(context: Context):
        context.actions.edit_message(GameSessionEntity.text_description(context))
        context.actions.edit_markup(GameSessionHandlers.build_main_menu(context))

    @staticmethod
    def new_session(context: Context):
        GameSessionEntity.stop_current_session(context)
        # After previous step, new session will be created.
        GameSessionEntity.get_or_create(context)
        GameSessionHandlers.session_menu(context)

    @staticmethod
    def choose_player_for_session(context: Context):
        player_id = context.data.callback_data.data
        player = context.session.query(Player).filter(Player.id == player_id).one_or_none()
        if player is not None:
            game_session = GameSessionEntity.get_or_create(context)
            if player.game_session_id == game_session.id:
                player.game_session_id = None
            else:
                player.game_session_id = game_session.id
            context.session.commit()
        GameSessionHandlers.session_menu(context)
