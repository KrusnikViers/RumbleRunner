from app.api.command_list import CallbackId, PendingRequestId
from app.handlers import *
from base import CallbackHandlerReg, CommandHandlerReg, PendingRequestHandlerReg, ChatType
from base.handler.default import canceling

ROUTING_LIST = [
    CallbackHandlerReg(CallbackId.COMMON_DELETE_MESSAGE,
                       canceling.delete_message),
    CallbackHandlerReg(CallbackId.COMMON_DELETE_MESSAGE_AND_PENDING_ACTION,
                       canceling.delete_message_and_pending_request),

    # Add your instances of CallbackHandlerReg and CommandHandlerReg in this list to be picked up by the dispatching.
    CommandHandlerReg(['trueskill', 'play'], MainMenuHandlers.open, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.MAIN_MENU_OPEN, MainMenuHandlers.open, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.MAIN_MENU_REDRAW, MainMenuHandlers.redraw, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.MAIN_MENU_STOP_SESSION, MainMenuHandlers.stop_session, ChatType.GROUP),

    CallbackHandlerReg(CallbackId.MATCHUP_SELECTION_OPEN, MatchupSelectionHandlers.open, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.MATCHUP_SELECTION_REDRAW, MatchupSelectionHandlers.redraw, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.MATCHUP_SELECTION_CHOOSE_MATCHUP, MatchupSelectionHandlers.choose_matchup,
                       ChatType.GROUP),
    CallbackHandlerReg(CallbackId.MATCHUP_SELECTION_CHOOSE_WINNER_TEAM, MatchupSelectionHandlers.choose_winner_team,
                       ChatType.GROUP),

    CallbackHandlerReg(CallbackId.MATCHUP_SELECTION_CUSTOM_WINNERS_REDRAW,
                       MatchupSelectionHandlers.custom_winners_redraw, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.MATCHUP_SELECTION_CUSTOM_WINNERS_SWITCH,
                       MatchupSelectionHandlers.custom_winners_switch, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.MATCHUP_SELECTION_CUSTOM_WINNERS_CONFIRM,
                       MatchupSelectionHandlers.custom_winners_confirm, ChatType.GROUP),

    CallbackHandlerReg(CallbackId.SESSION_PLAYERS_OPEN, SessionPlayersHandlers.open, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.SESSION_PLAYERS_REDRAW, SessionPlayersHandlers.redraw, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.SESSION_PLAYERS_NEW, SessionPlayersHandlers.new, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.SESSION_PLAYERS_SELECT, SessionPlayersHandlers.select, ChatType.GROUP),

    CallbackHandlerReg(CallbackId.PLAYERS_LIST_OPEN, PlayersListHandlers.open, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.PLAYERS_LIST_REDRAW, PlayersListHandlers.redraw, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.PLAYERS_LIST_PLAYER_CREATION_START, PlayersListHandlers.player_creation_start,
                       ChatType.GROUP),
    PendingRequestHandlerReg(PendingRequestId.PLAYERS_LIST_PLAYER_CREATION_NAME,
                             PlayersListHandlers.player_creation_name),
    CallbackHandlerReg(CallbackId.PLAYERS_LIST_PLAYER_CREATION_CANCEL, PlayersListHandlers.player_creation_cancel,
                       ChatType.GROUP),

    CallbackHandlerReg(CallbackId.PLAYER_PROFILE_OPEN, PlayerProfileHandlers.open, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.PLAYER_PROFILE_REDRAW, PlayerProfileHandlers.redraw, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.PLAYER_PROFILE_RENAMING_START, PlayerProfileHandlers.renaming_start, ChatType.GROUP),
    PendingRequestHandlerReg(PendingRequestId.PLAYER_PROFILE_RENAMING_NAME, PlayerProfileHandlers.renaming_name),
    CallbackHandlerReg(CallbackId.PLAYER_PROFILE_RENAMING_CANCEL, PlayerProfileHandlers.renaming_cancel,
                       ChatType.GROUP),
    CallbackHandlerReg(CallbackId.PLAYER_PROFILE_SCORE_RESET, PlayerProfileHandlers.score_reset, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.PLAYER_PROFILE_DELETE, PlayerProfileHandlers.delete, ChatType.GROUP)
]
