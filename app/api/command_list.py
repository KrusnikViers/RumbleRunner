# Namespace to store callback command ids and pending action ids. Callback id is tied to callbacks routing.
# Place to store custom PendingActions values. Pending request is a scheduled action, when you are waiting for the
# user input. If user has any pending action and text message from the user was received, corresponding handler
# will be executed for this message. Remember to clean pending action, if input was sufficient!
from enum import Enum, IntEnum, unique


@unique
class PendingRequestId(str, Enum):
    EXAMPLE_DUMMY_TYPE = 'dummy'

    # Place your custom pending request types below
    TS_NEW_PLAYER_NAME = 'new_player_name'
    TS_RENAME_PLAYER_NAME = 'rename_player_name'


@unique
class CallbackId(IntEnum):
    COMMON_DELETE_MESSAGE = 0
    COMMON_DELETE_MESSAGE_AND_PENDING_ACTION = 1

    # Add custom command codes here
    TS_MAIN_MENU = 100
    TS_STOP_SESSION = 101

    TS_PLAYERS_MENU = 110
    TS_NEW_PLAYER = 111
    TS_CANCEL_NEW_PLAYER = 112

    TS_PLAYER_MENU = 120
    TS_RENAME_PLAYER = 121
    TS_CANCEL_RENAME_PLAYER = 122
    TS_RESET_SCORE = 123
    TS_DELETE_PLAYER = 124

    TS_SESSION_MENU = 130
    TS_NEW_SESSION = 131
    TS_CHOOSE_PLAYER_FOR_SESSION = 132

    TS_MATCH_MENU = 140
