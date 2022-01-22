from app.api.command_list import CallbackId, PendingRequestId
from app.core.entities.game_ranking import GameRankingEntity
from app.core.entities.player import PlayerEntity
from app.core.rankings.trueskill import DEFAULT_MU, DEFAULT_SIGMA
from app.models.all import Player
from base.api.handler import Context, InlineMenu, InlineMenuButton
from base.api.routing import PendingRequests


class PlayerHandlers:
    @staticmethod
    def build_players_menu(context: Context):
        menu = []
        game_ranking = GameRankingEntity.get_or_create(context)
        players = PlayerEntity.get_for_ranking(context, game_ranking)
        for player in players:
            menu.append([InlineMenuButton(player.name, CallbackId.TS_PLAYER_MENU, player.id)])
        menu.append([InlineMenuButton('New player..', CallbackId.TS_NEW_PLAYER)])
        menu.append([InlineMenuButton('Back', CallbackId.TS_MAIN_MENU)])
        return InlineMenu(menu, user_tg_id=context.sender.tg_id)

    @staticmethod
    def build_player_menu(context: Context, player_id: int):
        return InlineMenu([
            [InlineMenuButton('Rename..', CallbackId.TS_RENAME_PLAYER, str(player_id))],
            [
                InlineMenuButton('Reset ranking stats', CallbackId.TS_RESET_SCORE, str(player_id)),
                InlineMenuButton('Delete forever', CallbackId.TS_DELETE_PLAYER, str(player_id))
            ],
            [InlineMenuButton('Back', CallbackId.TS_PLAYERS_MENU)]
        ])

    @staticmethod
    def players_menu(context: Context):
        context.actions.edit_message('Our heroes:')
        context.actions.edit_markup(PlayerHandlers.build_players_menu(context))

    @staticmethod
    def new_player(context: Context):
        PendingRequests.replace(context, PendingRequestId.TS_NEW_PLAYER_NAME)
        context.actions.edit_message('Write name for the new player')
        context.actions.edit_markup(InlineMenu([[InlineMenuButton('Cancel', CallbackId.TS_CANCEL_NEW_PLAYER)]],
                                               user_tg_id=context.sender.tg_id))

    @staticmethod
    def new_player_name(context: Context):
        new_name = context.data.text.strip()
        if not new_name:
            return 'Empty name? Try again'
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

    @staticmethod
    def player_menu(context: Context, player_id=None):
        if player_id is None:
            player_id = context.data.callback_data.data
        player = context.session.query(Player).filter(Player.id == player_id).one_or_none()
        if player is None:
            PlayerHandlers.players_menu(context)
            return

        context.actions.edit_message('Howdy, {}?\n\nMatches played: {}'.format(player.name, len(player.participations)))
        context.actions.edit_markup(PlayerHandlers.build_player_menu(context, player_id))

    @staticmethod
    def rename_player(context: Context):
        player = context.session.query(Player).filter(Player.id == context.data.callback_data.data).one_or_none()
        if player:
            PendingRequests.replace(context, PendingRequestId.TS_RENAME_PLAYER_NAME, str(player.id))
            context.actions.edit_message('Write new name for the {}:'.format(player.name))
            context.actions.edit_markup(InlineMenu([[InlineMenuButton('Cancel', CallbackId.TS_CANCEL_RENAME_PLAYER)]],
                                                   user_tg_id=context.sender.tg_id))
        else:
            context.actions.edit_markup(PlayerHandlers.player_menu(context))

    @staticmethod
    def rename_player_name(context: Context):
        new_name = context.data.text.strip()
        if not new_name:
            return 'Empty name? Try again'
        player_id = context.pending_request.additional_data
        player = context.session.query(Player).filter(Player.id == player_id).one_or_none()
        if player:
            player.name = new_name
            context.session.commit()
        context.actions.msg_id = context.pending_request.original_message_id
        context.session.delete(context.pending_request)
        PlayerHandlers.player_menu(context, player_id)

    @staticmethod
    def cancel_player_rename(context: Context):
        pending_request = PendingRequests.get(context)
        player_id = context.pending_request.additional_data
        if pending_request:
            context.session.delete(pending_request)
        PlayerHandlers.player_menu(context, player_id)

    @staticmethod
    def reset_score(context: Context):
        player = context.session.query(Player).filter(Player.id == context.data.callback_data.data).one_or_none()
        if player:
            player.mu = DEFAULT_MU
            player.sigma = DEFAULT_SIGMA
        PlayerHandlers.player_menu(context)

    @staticmethod
    def delete_player(context: Context):
        player = context.session.query(Player).filter(Player.id == context.data.callback_data.data).one_or_none()
        if player:
            context.session.delete(player)
            context.session.commit()
            PlayerHandlers.players_menu(context)
