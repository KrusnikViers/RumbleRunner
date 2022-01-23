from app.api.command_list import CallbackId
from app.core.entities.game_session import GameSessionEntity
from app.core.entities.player import PlayerEntity
from app.core.rankings.trueskill import TSClient, Matchup
from app.models.all import Participation
from base.api.handler import Context, InlineMenu, InlineMenuButton


class MatchmakingHandlers:
    @staticmethod
    def _get_matchup_markers(matchup: Matchup):
        result = ''
        if matchup.satisfaction >= 0:
            result += '❤'
        else:
            result += '💔'
        if matchup.quality >= 0.55:
            result += '🟢'
        elif matchup.quality > 0.25:
            result += '🟡'
        else:
            result += '🔴'
        result += ' {} {}-{}'.format(round(matchup.quality, 2),
                                     round(matchup.win_chance, 2), round(matchup.reverse_win_chance, 2))
        return result

    @staticmethod
    def _encode_teams(team_1: list, team_2: list) -> str:
        return '{} {} {}'.format(len(team_1),
                                 ' '.join([str(x) for x in team_1]),
                                 ' '.join([str(x) for x in team_2]))

    @staticmethod
    def _decode_teams(data: str) -> (list, list):
        data = [int(x) for x in data.split()]
        return data[1:1 + data[0]], data[1 + data[0]:]

    @staticmethod
    def _update_players(context: Context, team_won: list, team_lost: list):
        current_session = GameSessionEntity.get(context)
        players = PlayerEntity.get_id_map_for_session(context)

        for player_id in team_won:
            context.session.add(Participation(is_winner=True, player_id=player_id,
                                              game_session_id=current_session.id,
                                              match_number=current_session.matches_played))
        for player_id in team_lost:
            context.session.add(Participation(is_winner=False, player_id=player_id,
                                              game_session_id=current_session.id,
                                              match_number=current_session.matches_played))
        current_session.matches_played += 1

        TSClient.update_players_stats([players[player_id] for player_id in team_won],
                                      [players[player_id] for player_id in team_lost])

    @staticmethod
    def build_matchmaking_menu(context: Context):
        menu = []
        players = PlayerEntity.get_id_map_for_session(context)
        if len(players) >= 2:
            matchups = TSClient.get_matchups(context.session, GameSessionEntity.get(context))[:5]
            for matchup in matchups:
                text = '{} vs {} : {}'.format(
                    ', '.join([players[player.id].name for player in matchup.team_1]),
                    ', '.join([players[player.id].name for player in matchup.team_2]),
                    MatchmakingHandlers._get_matchup_markers(matchup)
                )
                callback_data = MatchmakingHandlers._encode_teams([player.id for player in matchup.team_1],
                                                                  [player.id for player in matchup.team_2])
                menu.append([
                    InlineMenuButton(text, CallbackId.TS_CHOOSE_TEAM_SETUP, callback_data)
                ])
            menu.append([InlineMenuButton('Play with custom teams..', CallbackId.TS_CUSTOM_TEAM_SETUP_MENU)])
        menu.append([InlineMenuButton('Cancel', CallbackId.TS_MAIN_MENU)])
        return InlineMenu(menu, user_tg_id=context.sender.tg_id)

    @staticmethod
    def matchmaking_menu(context: Context):
        game_session = GameSessionEntity.get(context)
        if len(PlayerEntity.get_for_session(context)) < 2:
            context.actions.edit_message('Not enough players in session!')
        else:
            context.actions.edit_message('Choose your destiny!\nMatch #{}'.format(game_session.matches_played))
        context.actions.edit_markup(MatchmakingHandlers.build_matchmaking_menu(context))

    @staticmethod
    def choose_team_setup(context: Context):
        players = PlayerEntity.get_id_map_for_session(context)
        team_1, team_2 = MatchmakingHandlers._decode_teams(context.data.callback_data.data)
        menu = InlineMenu([
            [InlineMenuButton(', '.join([players[id].name for id in team_1]), CallbackId.TS_CHOOSE_WINNER_TEAM,
                              MatchmakingHandlers._encode_teams(team_1, team_2))],
            [InlineMenuButton(', '.join([players[id].name for id in team_2]), CallbackId.TS_CHOOSE_WINNER_TEAM,
                              MatchmakingHandlers._encode_teams(team_2, team_1))],
            [InlineMenuButton('Back', CallbackId.TS_MATCHMAKING_MENU)]
        ], user_tg_id=context.sender.tg_id)
        context.actions.edit_message('Choose the winners:')
        context.actions.edit_markup(menu)

    @staticmethod
    def choose_winner_team(context: Context):
        team_won, team_lost = MatchmakingHandlers._decode_teams(context.data.callback_data.data)
        MatchmakingHandlers._update_players(context, team_won, team_lost)
        MatchmakingHandlers.matchmaking_menu(context)

    @staticmethod
    def custom_team_setup_menu(context: Context, winners_list=None):
        if winners_list is None:
            winners_list = []
        players = PlayerEntity.get_for_session(context)
        menu = []
        for player in players:
            text = ('✅ {}' if player.id in winners_list else '{}').format(player.name)
            data = winners_list[:].remove(player.id) if player.id in winners_list else [winners_list] + [player.id]
            menu.append([
                InlineMenuButton(text, CallbackId.TS_CUSTOM_TEAM_SETUP_CHOOSE_PLAYER, data)
            ])

        menu.append([InlineMenuButton('Confirm', CallbackId.TS_CUSTOM_TEAM_SETUP_CONFIRM, winners_list)])
        menu.append([InlineMenuButton('Cancel', CallbackId.TS_MATCHMAKING_MENU)])
        context.actions.edit_message('Choose your winners:')
        context.actions.edit_markup(InlineMenu(menu, user_tg_id=context.sender.tg_id))

    @staticmethod
    def custom_team_setup_choose_player(context: Context):
        winners = [int(x) for x in context.data.callback_data.data.split()]
        MatchmakingHandlers.custom_team_setup_menu(context, winners)

    @staticmethod
    def custom_team_setup_confirm(context: Context):
        team_won = [int(x) for x in context.data.callback_data.data.split()]
        all_players = PlayerEntity.get_for_session(context)
        team_lost = [player.id for player in all_players if player.id not in team_won]
        MatchmakingHandlers._update_players(context, team_won, team_lost)
        MatchmakingHandlers.matchmaking_menu(context)
