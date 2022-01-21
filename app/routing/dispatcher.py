from app.routing.callbacks import CallbackIds
from base.api.routing import CallbackHandlerReg
from base.handler.default import canceling

UPDATE_HANDLERS = [
    CallbackHandlerReg(CallbackIds.COMMON_DELETE_MESSAGE,
                       canceling.delete_message),
    CallbackHandlerReg(CallbackIds.COMMON_DELETE_MESSAGE_AND_PENDING_ACTION,
                       canceling.delete_message_and_pending_request),

    # Add your instances of CallbackHandlerReg and CommandHandlerReg in this list to be picked up by the dispatching.
]
