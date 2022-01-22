# Place to store custom PendingActions values. Pending action is a scheduled action, when you are waiting for the
# user input. To create new action, add new value in |PendingActions| class and new handler function, so that
# dispatcher would know how to process it.
# If user has any pending action and received any message from the user, corresponding handler will be executed
# for this message. Remember to clean pending action, if it was the message you were expecting!
from enum import unique, Enum


@unique
class PendingRequestType(str, Enum):
    EXAMPLE_DUMMY_TYPE = 'dummy'

    # Place your custom pending request types below
    TS_NEW_PLAYER_NAME = 'new_player_name'
