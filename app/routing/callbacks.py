# Namespace to store command ids. Callback command id should be provided while constructing inline menu, and they
# should be unique among each other.
from enum import IntEnum, unique


@unique
class CallbackIds(IntEnum):
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
    TS_CANCEL_RENAME = 122
    TS_RESET_SCORE = 123
    TS_DELETE_PLAYER = 124

    TS_SESSION_MENU = 130
    TS_NEW_SESSION = 131
    TS_CHOOSE_PLAYER_FOR_SESSION = 132

    TS_MATCH_MENU = 140
