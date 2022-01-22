from app.api.command_list import CallbackId, PendingRequestId
from app.core.handlers.game_ranking import GameRankingHandlers
from app.core.handlers.game_session import GameSessionHandlers
from app.core.handlers.player import PlayerHandlers
from base.api.routing import CallbackHandlerReg, CommandHandlerReg, PendingRequestHandlerReg, ChatType
from base.handler.default import canceling

ROUTING_LIST = [
    CallbackHandlerReg(CallbackId.COMMON_DELETE_MESSAGE,
                       canceling.delete_message),
    CallbackHandlerReg(CallbackId.COMMON_DELETE_MESSAGE_AND_PENDING_ACTION,
                       canceling.delete_message_and_pending_request),

    # Add your instances of CallbackHandlerReg and CommandHandlerReg in this list to be picked up by the dispatching.
    CommandHandlerReg(['trueskill'], GameRankingHandlers.main_menu, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.TS_MAIN_MENU, GameRankingHandlers.main_menu_callback),
    CallbackHandlerReg(CallbackId.TS_STOP_SESSION, GameRankingHandlers.stop_session),

    CallbackHandlerReg(CallbackId.TS_PLAYERS_MENU, PlayerHandlers.players_menu),
    CallbackHandlerReg(CallbackId.TS_NEW_PLAYER, PlayerHandlers.new_player),
    PendingRequestHandlerReg(PendingRequestId.TS_NEW_PLAYER_NAME, PlayerHandlers.new_player_name),
    CallbackHandlerReg(CallbackId.TS_CANCEL_NEW_PLAYER, PlayerHandlers.cancel_new_player),

    CallbackHandlerReg(CallbackId.TS_PLAYER_MENU, PlayerHandlers.player_menu),
    CallbackHandlerReg(CallbackId.TS_RENAME_PLAYER, PlayerHandlers.rename_player),
    PendingRequestHandlerReg(PendingRequestId.TS_RENAME_PLAYER_NAME, PlayerHandlers.rename_player_name),
    CallbackHandlerReg(CallbackId.TS_CANCEL_RENAME_PLAYER, PlayerHandlers.cancel_player_rename),
    CallbackHandlerReg(CallbackId.TS_RESET_SCORE, PlayerHandlers.reset_score),
    CallbackHandlerReg(CallbackId.TS_DELETE_PLAYER, PlayerHandlers.delete_player),

    CallbackHandlerReg(CallbackId.TS_SESSION_MENU, GameSessionHandlers.session_menu),
    CallbackHandlerReg(CallbackId.TS_NEW_SESSION, GameSessionHandlers.new_session),
    CallbackHandlerReg(CallbackId.TS_CHOOSE_PLAYER_FOR_SESSION, GameSessionHandlers.choose_player_for_session),
]
