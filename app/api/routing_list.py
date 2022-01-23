from app.api.command_list import CallbackId, PendingRequestId
from app.handlers.game_ranking import GameRankingHandlers
from app.handlers.game_session import GameSessionHandlers
from app.handlers.matchmaking import MatchmakingHandlers
from app.handlers.player import PlayerHandlers
from base.api.routing import CallbackHandlerReg, CommandHandlerReg, PendingRequestHandlerReg, ChatType
from base.handler.default import canceling

ROUTING_LIST = [
    CallbackHandlerReg(CallbackId.COMMON_DELETE_MESSAGE,
                       canceling.delete_message),
    CallbackHandlerReg(CallbackId.COMMON_DELETE_MESSAGE_AND_PENDING_ACTION,
                       canceling.delete_message_and_pending_request),

    # Add your instances of CallbackHandlerReg and CommandHandlerReg in this list to be picked up by the dispatching.
    CommandHandlerReg(['trueskill', 'play'], GameRankingHandlers.open_menu, ChatType.GROUP),
    CallbackHandlerReg(CallbackId.TS_RANKING_OPEN_MENU, GameRankingHandlers.open_menu_callback),
    CallbackHandlerReg(CallbackId.TS_RANKING_STOP_GAME_SESSION, GameRankingHandlers.stop_game_session),

    CallbackHandlerReg(CallbackId.TS_PLAYERS_MANAGEMENT_OPEN_MENU, PlayerHandlers.management_open_menu),
    CallbackHandlerReg(CallbackId.TS_PLAYERS_MANAGEMENT_START_PLAYER_CREATION, PlayerHandlers.start_player_creation),
    CallbackHandlerReg(CallbackId.TS_PLAYERS_MANAGEMENT_CANCEL_PLAYER_CREATION, PlayerHandlers.cancel_player_creation),
    PendingRequestHandlerReg(PendingRequestId.TS_PLAYERS_MANAGEMENT_PLAYER_CREATION_NAME,
                             PlayerHandlers.player_creation_name),

    CallbackHandlerReg(CallbackId.TS_PLAYER_OPEN_MENU, PlayerHandlers.open_menu),
    CallbackHandlerReg(CallbackId.TS_PLAYER_START_RENAMING, PlayerHandlers.start_renaming),
    CallbackHandlerReg(CallbackId.TS_PLAYER_CANCEL_RENAMING, PlayerHandlers.cancel_renaming),
    CallbackHandlerReg(CallbackId.TS_PLAYER_RESET_SCORE, PlayerHandlers.reset_score),
    CallbackHandlerReg(CallbackId.TS_PLAYER_DELETE, PlayerHandlers.delete),
    PendingRequestHandlerReg(PendingRequestId.TS_PLAYER_RENAMING_NAME, PlayerHandlers.renaming_name),

    CallbackHandlerReg(CallbackId.TS_GAME_SESSION_OPEN_MENU, GameSessionHandlers.open_menu),
    CallbackHandlerReg(CallbackId.TS_GAME_SESSION_CREATE_NEW, GameSessionHandlers.create_new),
    CallbackHandlerReg(CallbackId.TS_GAME_SESSION_CHOOSE_PLAYER, GameSessionHandlers.choose_player),

    CallbackHandlerReg(CallbackId.TS_MATCH_OPEN_MENU, MatchmakingHandlers.open_menu),
    CallbackHandlerReg(CallbackId.TS_MATCH_CHOOSE_MATCHUP, MatchmakingHandlers.choose_matchup),
    CallbackHandlerReg(CallbackId.TS_MATCH_CHOOSE_WINNERS, MatchmakingHandlers.choose_winners),
    CallbackHandlerReg(CallbackId.TS_MATCH_CUSTOM_TEAM_OPEN_MENU, MatchmakingHandlers.custom_team_open_menu),
    CallbackHandlerReg(CallbackId.TS_MATCH_CUSTOM_TEAM_CHOOSE_PLAYER,
                       MatchmakingHandlers.custom_team_choose_player),
    CallbackHandlerReg(CallbackId.TS_MATCH_CUSTOM_TEAM_CONFIRM, MatchmakingHandlers.custom_team_confirm),
]
