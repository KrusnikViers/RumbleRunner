from app.routing.callbacks import CallbackIds
from base.api.routing import CallbackHandlerReg
from base.handler.default import canceling

UPDATE_HANDLERS = [
    CallbackHandlerReg(CallbackIds.COMMON_DELETE_MESSAGE,
                       canceling.delete_message),
    CallbackHandlerReg(CallbackIds.COMMON_DELETE_MESSAGE_AND_PENDING_ACTION,
                       canceling.delete_message_and_pending_request),

    # Add your instances of CallbackHandlerReg and CommandHandlerReg in this list to be picked up by the dispatching.
    # CommandHandlerReg(['create_player'], player_management.create_player),
    # CommandHandlerReg(['delete_player'], player_management.delete_player),
    # CallbackHandlerReg(CallbackIds.PM_DELETE_PLAYER,
    #                    player_management.delete_player_callback),
    #
    # CommandHandlerReg(['create_session'], matchmaking.start_new_session),
    # CommandHandlerReg(['update_session'], matchmaking.update_session),
    # CallbackHandlerReg(CallbackIds.MM_SWITCH_PLAYER_SESSION_STATUS, matchmaking.switch_player_status),
    # CallbackHandlerReg(CallbackIds.MM_CANCEL_NEW_SESSION, matchmaking.cancel_session_creation),
    # CallbackHandlerReg(CallbackIds.MM_CONFIRM_NEW_SESSION, matchmaking.confirm_session_creation),

]
