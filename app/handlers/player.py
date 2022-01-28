from app.api.command_list import CallbackId, PendingRequestId
from app.core.game_ranking import GameRankingHelpers
from app.core.player import PlayerHelpers
from app.core.trueskill import TrueSkillParams
from app.models.all import Player
from base.api.database import SessionScope
from base.api.handler import Context, InlineMenu, InlineMenuButton, Actions
from base.api.routing import Requests


class PlayerHandlers:
    @staticmethod
    def build_players_menu(context: Context):
        menu = []
        players = PlayerHelpers.get_for_ranking(context)
        for player in players:
            menu.append([InlineMenuButton(player.name, CallbackId.TS_PLAYER_OPEN_MENU, player.id)])
        menu.append([InlineMenuButton('New player..', CallbackId.TS_PLAYERS_MANAGEMENT_START_PLAYER_CREATION)])
        menu.append([InlineMenuButton('Back', CallbackId.TS_RANKING_OPEN_MENU)])
        return InlineMenu(menu, user_tg_id=context.sender.tg_id)

    @staticmethod
    def build_player_menu(context: Context, player_id: int):
        return InlineMenu([
            [InlineMenuButton('Rename..', CallbackId.TS_PLAYER_START_RENAMING, str(player_id))],
            [
                InlineMenuButton('Reset ranking stats', CallbackId.TS_PLAYER_RESET_SCORE, str(player_id)),
                InlineMenuButton('Delete forever', CallbackId.TS_PLAYER_DELETE, str(player_id))
            ],
            [InlineMenuButton('Back', CallbackId.TS_PLAYERS_MANAGEMENT_OPEN_MENU)]
        ])

    @staticmethod
    def management_open_menu(context: Context):
        Actions.edit_message('Our heroes:')
        Actions.edit_markup(PlayerHandlers.build_players_menu(context))

    @staticmethod
    def start_player_creation(context: Context):
        Requests.replace(context, PendingRequestId.TS_PLAYERS_MANAGEMENT_PLAYER_CREATION_NAME)
        Actions.edit_message('Write name for the new player')
        Actions.edit_markup(
            InlineMenu([[InlineMenuButton('Cancel', CallbackId.TS_PLAYERS_MANAGEMENT_CANCEL_PLAYER_CREATION)]],
                       user_tg_id=context.sender.tg_id))

    @staticmethod
    def player_creation_name(context: Context):
        new_name = context.message.data.strip()
        if not new_name:
            return 'Empty name? Try again'
        game_ranking = GameRankingHelpers.get_or_create(context)
        SessionScope.session().add(
            Player(name=new_name, mu=TrueSkillParams.DEFAULT_MU, sigma=TrueSkillParams.DEFAULT_SIGMA,
                   game_ranking_id=game_ranking.id))
        SessionScope.commit()
        Actions.msg_id = context.request.original_message_id
        SessionScope.session().delete(context.request)
        PlayerHandlers.management_open_menu(context)

    @staticmethod
    def cancel_player_creation(context: Context):
        pending_request = context.request
        if pending_request:
            SessionScope.session().delete(pending_request)
        PlayerHandlers.management_open_menu(context)

    @staticmethod
    def open_menu(context: Context, player_id=None):
        if player_id is None:
            player_id = context.message.data
        player = SessionScope.session().query(Player).filter(Player.id == player_id).one_or_none()
        if player is None:
            PlayerHandlers.management_open_menu(context)
            return

        skill_confidence = 1.0 - player.sigma / (TrueSkillParams.DEFAULT_SIGMA * 2)
        Actions.edit_message('Howdy, {}?\n\nMatches played: {}\nSkill confidence: {}%'.format(
            player.name, len(player.participations), int(skill_confidence * 100.0)), message=context.message)
        Actions.edit_markup(PlayerHandlers.build_player_menu(context, player_id), message=context.message)

    @staticmethod
    def start_renaming(context: Context):
        player = SessionScope.session().query(Player).filter(Player.id == context.data.callback_data.data).one_or_none()
        if player:
            Requests.replace(context, PendingRequestId.TS_PLAYER_RENAMING_NAME, str(player.id))
            Actions.edit_message('Write new name for the {}:'.format(player.name), message=context.message)
            Actions.edit_markup(InlineMenu([[InlineMenuButton('Cancel', CallbackId.TS_CANCEL_PLAYER_RENAMING)]],
                                           user_tg_id=context.sender.tg_id), message=context.message)
        else:
            Actions.edit_markup(PlayerHandlers.open_menu(context), message=context.message)

    @staticmethod
    def renaming_name(context: Context):
        new_name = context.message.data.strip()
        if not new_name:
            return 'Empty name? Try again'
        player_id = context.request.additional_data
        player = SessionScope.session().query(Player).filter(Player.id == player_id).one_or_none()
        if player:
            player.name = new_name
            SessionScope.commit()
        Actions.msg_id = context.request.original_message_id
        SessionScope.session().delete(context.request)
        PlayerHandlers.open_menu(context, player_id)

    @staticmethod
    def cancel_renaming(context: Context):
        pending_request = context.request
        player_id = context.request.additional_data
        if pending_request:
            SessionScope.session().delete(pending_request)
        PlayerHandlers.open_menu(context, player_id)

    @staticmethod
    def reset_score(context: Context):
        player = SessionScope.session().query(Player).filter(Player.id == context.message.data).one_or_none()
        if player:
            player.mu = TrueSkillParams.DEFAULT_MU
            player.sigma = TrueSkillParams.DEFAULT_SIGMA
        PlayerHandlers.open_menu(context)

    @staticmethod
    def delete(context: Context):
        player = SessionScope.session().query(Player).filter(Player.id == context.message.data).one_or_none()
        if player:
            SessionScope.session().delete(player)
            SessionScope.commit()
            PlayerHandlers.management_open_menu(context)
