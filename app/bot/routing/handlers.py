from app.bot.core.handlers import common, player_management
from app.bot.routing.callbacks import CallbackIds
from app.public.handlers import CallbackHandlerReg, CommandHandlerReg, FilterType

HANDLERS = [
    # Add your instances of CallbackHandlerReg and CommandHandlerReg in this list to be picked up by the dispatching.
    CallbackHandlerReg(CallbackIds.COMMON_CANCEL_DELETE_MESSAGE,
                       common.cancel_delete_message_callback),
    CallbackHandlerReg(CallbackIds.COMMON_CANCEL_DELETE_MESSAGE_PERSONAL,
                       common.cancel_delete_message_callback, [FilterType.PERSONAL_CALLBACK]),

    CommandHandlerReg(['create_player'], player_management.create_player),
    CommandHandlerReg(['delete_player'], player_management.delete_player),
    CallbackHandlerReg(CallbackIds.PM_DELETE_PLAYER,
                       player_management.delete_player_callback, [FilterType.PERSONAL_CALLBACK])

]
