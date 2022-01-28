# Namespace to store callback command ids and pending action ids. Callback id is tied to callbacks routing.
# Place to store custom PendingActions values. Pending request is a scheduled action, when you are waiting for the
# user input. If user has any pending action and text message from the user was received, corresponding handler
# will be executed for this message. Remember to clean pending action, if input was sufficient!
import logging
from enum import Enum, IntEnum, unique
from typing import Optional, TypeVar, Type

IdType = TypeVar('IdType')


def value_to_enum(id_type: Type[IdType], value) -> Optional[IdType]:
    try:
        result = id_type(value)
        return result
    except ValueError:
        logging.warning("Bad value {} for conversion into {}".format(value, id_type))
        return None


@unique
class PendingRequestId(str, Enum):
    PREDEFINED_FOR_TESTS_1 = 'dummy_1'
    PREDEFINED_FOR_TESTS_2 = 'dummy_2'

    # Place your custom pending request types below
    TS_PLAYERS_MANAGEMENT_PLAYER_CREATION_NAME = 'player_creation_name'
    TS_PLAYER_RENAMING_NAME = 'renaming_name'


@unique
class CallbackId(IntEnum):
    COMMON_DELETE_MESSAGE = 0
    COMMON_DELETE_MESSAGE_AND_PENDING_ACTION = 1

    # Add custom command codes here
    TS_RANKING_OPEN_MENU = 100
    TS_RANKING_STOP_GAME_SESSION = 101

    TS_PLAYERS_MANAGEMENT_OPEN_MENU = 110
    TS_PLAYERS_MANAGEMENT_START_PLAYER_CREATION = 111
    TS_PLAYERS_MANAGEMENT_CANCEL_PLAYER_CREATION = 112

    TS_PLAYER_OPEN_MENU = 120
    TS_PLAYER_START_RENAMING = 121
    TS_PLAYER_CANCEL_RENAMING = 122
    TS_PLAYER_RESET_SCORE = 123
    TS_PLAYER_DELETE = 124

    TS_GAME_SESSION_OPEN_MENU = 130
    TS_GAME_SESSION_CREATE_NEW = 131
    TS_GAME_SESSION_CHOOSE_PLAYER = 132

    TS_MATCH_OPEN_MENU = 140
    TS_MATCH_CHOOSE_MATCHUP = 141
    TS_MATCH_CHOOSE_WINNERS = 142
    TS_MATCH_CUSTOM_TEAM_OPEN_MENU = 143
    TS_MATCH_CUSTOM_TEAM_CHOOSE_PLAYER = 144
    TS_MATCH_CUSTOM_TEAM_CONFIRM = 145
