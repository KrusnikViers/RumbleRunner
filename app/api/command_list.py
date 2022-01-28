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
    PLAYERS_LIST_PLAYER_CREATION_NAME = 'PLAYERS_LIST_PLAYER_CREATION_NAME'
    PLAYER_PROFILE_RENAMING_NAME = 'PLAYER_PROFILE_RENAMING_NAME'


@unique
class CallbackId(IntEnum):
    COMMON_DELETE_MESSAGE = 0
    COMMON_DELETE_MESSAGE_AND_PENDING_ACTION = 1

    # Add custom command codes here
    MAIN_MENU_OPEN = 100
    MAIN_MENU_REDRAW = 101
    MAIN_MENU_STOP_SESSION = 102

    MATCHUP_SELECTION_OPEN = 110
    MATCHUP_SELECTION_REDRAW = 111
    MATCHUP_SELECTION_CHOOSE_MATCHUP = 112
    MATCHUP_SELECTION_CHOOSE_WINNER_TEAM = 113

    MATCHUP_SELECTION_CUSTOM_WINNERS_REDRAW = 150
    MATCHUP_SELECTION_CUSTOM_WINNERS_SWITCH = 151
    MATCHUP_SELECTION_CUSTOM_WINNERS_CONFIRM = 152

    SESSION_PLAYERS_OPEN = 120
    SESSION_PLAYERS_REDRAW = 121
    SESSION_PLAYERS_NEW = 122
    SESSION_PLAYERS_SELECT = 123

    PLAYERS_LIST_OPEN = 130
    PLAYERS_LIST_REDRAW = 131
    PLAYERS_LIST_PLAYER_CREATION_START = 132
    PLAYERS_LIST_PLAYER_CREATION_CANCEL = 133

    PLAYER_PROFILE_OPEN = 140
    PLAYER_PROFILE_REDRAW = 141
    PLAYER_PROFILE_RENAMING_START = 142
    PLAYER_PROFILE_RENAMING_CANCEL = 143
    PLAYER_PROFILE_SCORE_RESET = 144
    PLAYER_PROFILE_DELETE = 145
