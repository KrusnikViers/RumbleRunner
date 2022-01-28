from typing import Optional

from app.api import CallbackId, PendingRequestId
from app.core import PlayerHelpers, TrueSkillParams
from app.handlers.players_list import PlayersListHandlers
from app.models import Player
from base import SessionScope, Context, InlineMenu, InlineMenuButton, Requests, Actions


class PlayerProfileHandlers:
    @staticmethod
    def _title(context, player: Player):
        skill_confidence = 1.0 - player.sigma / (TrueSkillParams.DEFAULT_SIGMA * 2)
        return ("Howdy, {}?\n\n"
                "Matches played: {}\n"
                "Skill confidence: {}%").format(player.name, len(player.participations), int(skill_confidence * 100))

    @staticmethod
    def _markup(context: Context, player: Player):
        return InlineMenu([
            [InlineMenuButton('Rename..', CallbackId.PLAYER_PROFILE_RENAMING_START, player.id)],
            [
                InlineMenuButton('Reset ranking', CallbackId.PLAYER_PROFILE_SCORE_RESET, player.id),
                InlineMenuButton('Delete forever', CallbackId.PLAYER_PROFILE_DELETE, player.id)
            ],
            [InlineMenuButton('Players list', CallbackId.PLAYERS_LIST_REDRAW)]
        ])

    @staticmethod
    def _fetch_player_or_fallback(context: Context) -> Optional[Player]:
        if (player := PlayerHelpers.by_id(context.message.data)) is not None:
            return player
        PlayersListHandlers.open(context)
        return None

    @staticmethod
    def open(context: Context):
        if player := PlayerProfileHandlers._fetch_player_or_fallback(context):
            if context.message.is_callback:
                context.delete_message()
            context.send_message(PlayerProfileHandlers._title(context, player),
                                 reply_markup=PlayerProfileHandlers._markup(context, player))

    @staticmethod
    def redraw(context: Context):
        if player := PlayerProfileHandlers._fetch_player_or_fallback(context):
            context.edit_message(PlayerProfileHandlers._title(context, player),
                                 reply_markup=PlayerProfileHandlers._markup(context, player))

    @staticmethod
    def renaming_start(context: Context):
        if player := PlayerProfileHandlers._fetch_player_or_fallback(context):
            context.delete_message()
            result_message = context.send_message(
                'New name for {}:'.format(player.name),
                reply_markup=context.personal_menu(
                    [[InlineMenuButton('Cancel', CallbackId.PLAYER_PROFILE_RENAMING_CANCEL)]]))
            Requests.replace(context, PendingRequestId.PLAYER_PROFILE_RENAMING_NAME,
                             result_message.message_id, player.id)

    @staticmethod
    def renaming_cancel(context: Context):
        Requests.delete(context)
        PlayerProfileHandlers.redraw(context)

    @staticmethod
    def renaming_name(context: Context):
        new_name = context.message.data.strip()
        if not new_name:
            return
        if player := PlayerHelpers.by_id(context.request.additional_data):
            player.name = new_name
            SessionScope.commit()
            Actions.delete_message(chat_id=context.message.chat_id, message_id=context.request.original_message_id)
            Requests.delete(context)
            PlayerProfileHandlers.open(context)

    @staticmethod
    def score_reset(context: Context):
        if player := PlayerProfileHandlers._fetch_player_or_fallback(context):
            player.mu = TrueSkillParams.DEFAULT_MU
            player.sigma = TrueSkillParams.DEFAULT_SIGMA
            SessionScope.commit()
        PlayerProfileHandlers.redraw(context)

    @staticmethod
    def delete(context: Context):
        if player := PlayerProfileHandlers._fetch_player_or_fallback(context):
            SessionScope.session().delete(player)
            SessionScope.commit()
        PlayersListHandlers.redraw(context)
