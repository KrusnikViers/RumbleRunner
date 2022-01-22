# Namespace to store command ids. Callback command id should be provided while constructing inline menu, and they
# should be unique among each other.
from enum import IntEnum, unique


@unique
class CallbackIds(IntEnum):
    COMMON_DELETE_MESSAGE = 0
    COMMON_DELETE_MESSAGE_AND_PENDING_ACTION = 1

    # Add custom command codes here
