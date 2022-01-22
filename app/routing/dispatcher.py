from app.core.handlers.game_ranking import GameRankingHandlers
from app.core.handlers.game_session import GameSessionHandlers
from app.core.handlers.player import PlayerHandlers
from app.routing.callbacks import CallbackIds
from app.routing.pending_requests import PendingRequestType
from base.api.routing import CallbackHandlerReg, CommandHandlerReg, PendingRequestHandlerReg, ChatType
from base.handler.default import canceling

HANDLERS_LIST = [
    CallbackHandlerReg(CallbackIds.COMMON_DELETE_MESSAGE,
                       canceling.delete_message),
    CallbackHandlerReg(CallbackIds.COMMON_DELETE_MESSAGE_AND_PENDING_ACTION,
                       canceling.delete_message_and_pending_request),

    # Add your instances of CallbackHandlerReg and CommandHandlerReg in this list to be picked up by the dispatching.
    CommandHandlerReg(['trueskill'], GameRankingHandlers.main_menu, ChatType.GROUP),
    CallbackHandlerReg(CallbackIds.TS_MAIN_MENU, GameRankingHandlers.main_menu_callback),
    CallbackHandlerReg(CallbackIds.TS_STOP_SESSION, GameRankingHandlers.stop_session),

    CallbackHandlerReg(CallbackIds.TS_PLAYERS_MENU, PlayerHandlers.players_menu),
    CallbackHandlerReg(CallbackIds.TS_NEW_PLAYER, PlayerHandlers.new_player),
    PendingRequestHandlerReg(PendingRequestType.TS_NEW_PLAYER_NAME, PlayerHandlers.new_player_name),
    CallbackHandlerReg(CallbackIds.TS_CANCEL_NEW_PLAYER, PlayerHandlers.cancel_new_player),

    CallbackHandlerReg(CallbackIds.TS_SESSION_MENU, GameSessionHandlers.session_menu),
    CallbackHandlerReg(CallbackIds.TS_NEW_SESSION, GameSessionHandlers.new_session),
    CallbackHandlerReg(CallbackIds.TS_CHOOSE_PLAYER_FOR_SESSION, GameSessionHandlers.choose_player_for_session),
]
