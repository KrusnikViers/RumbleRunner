from app.core.entities.game_ranking import GameRankingEntity
from app.core.entities.player import PlayerEntity
from app.core.rankings.trueskill import DEFAULT_MU, DEFAULT_SIGMA
from app.models.all import Player
from app.routing.callbacks import CallbackIds
from app.routing.pending_requests import PendingRequestType
from base.api.handler import Context, InlineMenu, InlineMenuButton
from base.api.routing import PendingRequests


# TS_PLAYERS_MENU = 110
# TS_NEW_PLAYER = 111
# TS_CANCEL_NEW_PLAYER = 112
#
# TS_PLAYER_MENU = 120
# TS_RENAME_PLAYER = 121
# TS_CANCEL_RENAME = 122
# TS_RESET_SCORE = 123
# TS_DELETE_PLAYER = 124


class PlayerHandlers:
    @staticmethod
    def build_players_menu(context: Context):
        menu = []
        game_ranking = GameRankingEntity.get_or_create(context)
        players = PlayerEntity.get_for_ranking(context, game_ranking)
        for player in players:
            menu.append([InlineMenuButton(player.name, CallbackIds.TS_PLAYER_MENU, player.id)])
        menu.append([InlineMenuButton('Create new player...', CallbackIds.TS_NEW_PLAYER)])
        menu.append([InlineMenuButton('Back', CallbackIds.TS_MAIN_MENU)])
        return InlineMenu(menu, user_tg_id=context.sender.tg_id)

    @staticmethod
    def players_menu(context: Context):
        context.actions.edit_message('Players management')
        context.actions.edit_markup(PlayerHandlers.build_players_menu(context))

    @staticmethod
    def new_player(context: Context):
        PendingRequests.replace(context, PendingRequestType.TS_NEW_PLAYER_NAME)
        context.actions.edit_message('Send me a name for the new player')
        context.actions.edit_markup(InlineMenu([[InlineMenuButton('Cancel', CallbackIds.TS_CANCEL_NEW_PLAYER)]],
                                               user_tg_id=context.sender.tg_id))

    @staticmethod
    def new_player_name(context: Context):
        new_name = context.data.text.strip()
        if not new_name:
            return 'Empty name; Please, try another one'
        game_ranking = GameRankingEntity.get_or_create(context)
        context.session.add(Player(name=new_name, mu=DEFAULT_MU, sigma=DEFAULT_SIGMA, game_ranking_id=game_ranking.id))
        context.session.commit()
        context.actions.msg_id = context.pending_request.original_message_id
        context.session.delete(context.pending_request)
        PlayerHandlers.players_menu(context)

    @staticmethod
    def cancel_new_player(context: Context):
        pending_request = PendingRequests.get(context)
        if pending_request:
            context.session.delete(pending_request)
        PlayerHandlers.players_menu(context)
