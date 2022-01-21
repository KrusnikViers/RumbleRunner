# Namespace to store command ids. Callback command id should be provided while constructing inline menu, and they
# should be unique among each other.
from enum import IntEnum, unique


@unique
class CallbackIds(IntEnum):
    COMMON_DELETE_MESSAGE = 0
    COMMON_DELETE_MESSAGE_AND_PENDING_ACTION = 1

    # Add custom command codes here
    PM_DELETE_PLAYER = 100

    MM_SWITCH_PLAYER_SESSION_STATUS = 200
    MM_CONFIRM_NEW_SESSION = 201
    MM_CANCEL_NEW_SESSION = 202
