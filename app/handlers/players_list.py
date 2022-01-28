from app.api import CallbackId, PendingRequestId
from app.core import GameRankingHelpers, PlayerHelpers, TrueSkillParams
from app.models import Player
from base import SessionScope, Context, InlineMenuButton, Requests, Actions


class PlayersListHandlers:
    @staticmethod
    def _title(context: Context):
        return "Total players: {}".format(len(PlayerHelpers.get_for_ranking(context)))

    @staticmethod
    def _markup(context: Context):
        menu = list()
        players = PlayerHelpers.get_for_ranking(context)
        for player in players:
            menu.append([InlineMenuButton(player.name, CallbackId.PLAYER_PROFILE_OPEN, player.id)])
        menu.append([InlineMenuButton('Create new..', CallbackId.PLAYERS_LIST_PLAYER_CREATION_START)])
        menu.append([InlineMenuButton('Main menu', CallbackId.MAIN_MENU_REDRAW)])
        return context.personal_menu(menu)

    @staticmethod
    def open(context: Context):
        if context.message.is_callback:
            context.delete_message()
        context.send_message(PlayersListHandlers._title(context), reply_markup=PlayersListHandlers._markup(context))

    @staticmethod
    def redraw(context: Context):
        context.edit_message(PlayersListHandlers._title(context), reply_markup=PlayersListHandlers._markup(context))

    @staticmethod
    def player_creation_start(context: Context):
        context.delete_message()
        result_message = context.send_message('Name for the new player:', reply_markup=context.personal_menu([[
            InlineMenuButton('Cancel', CallbackId.PLAYERS_LIST_PLAYER_CREATION_CANCEL)
        ]]))
        Requests.replace(context, PendingRequestId.PLAYERS_LIST_PLAYER_CREATION_NAME, result_message.message_id)

    @staticmethod
    def player_creation_cancel(context: Context):
        Requests.delete(context)
        PlayersListHandlers.redraw(context)

    @staticmethod
    def player_creation_name(context: Context):
        new_name = context.message.data.strip()
        if not new_name:
            return

        game_ranking = GameRankingHelpers.get_or_create(context)
        SessionScope.session().add(
            Player(name=new_name, mu=TrueSkillParams.DEFAULT_MU, sigma=TrueSkillParams.DEFAULT_SIGMA,
                   game_ranking_id=game_ranking.id))
        SessionScope.commit()

        Actions.delete_message(chat_id=context.message.chat_id, message_id=context.request.original_message_id)
        Requests.delete(context)
        PlayersListHandlers.open(context)
