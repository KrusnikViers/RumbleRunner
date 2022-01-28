from app.api.command_list import CallbackId
from app.core.game_session import GameSessionHelpers
from app.core.player import PlayerHelpers
from app.core.trueskill import TrueSkillClient, TrueSkillMatchup
from app.models.all import Participation
from base.api.database import SessionScope
from base.api.handler import Context, InlineMenu, InlineMenuButton, Actions


class MatchmakingHandlers:
    @staticmethod
    def _update_players(context: Context, team_won: list, team_lost: list):
        current_session = GameSessionHelpers.get(context)
        players = PlayerHelpers.get_id_map_for_session(context)

        for player_id in team_won:
            SessionScope.session().add(Participation(is_winner=True, player_id=player_id,
                                                     game_session_id=current_session.id,
                                                     match_number=current_session.matches_played))
        for player_id in team_lost:
            SessionScope.session().add(Participation(is_winner=False, player_id=player_id,
                                                     game_session_id=current_session.id,
                                                     match_number=current_session.matches_played))
        current_session.matches_played += 1

        TrueSkillClient.update_players([players[player_id] for player_id in team_won],
                                       [players[player_id] for player_id in team_lost])

    @staticmethod
    def _build_menu_markup(context: Context):
        menu = []
        players = PlayerHelpers.get_id_map_for_session(context)
        if len(players) >= 2:
            matchups = TrueSkillClient.calculate_matchups(context)[:5]
            for matchup in matchups:
                text = '{} vs {} : {}'.format(
                    ', '.join([players[player.id].name for player in matchup.team_1]),
                    ', '.join([players[player.id].name for player in matchup.team_2]),
                    MatchmakingHandlers._build_quality_markers_string(matchup)
                )
                callback_data = MatchmakingHandlers._encode_teams([player.id for player in matchup.team_1],
                                                                  [player.id for player in matchup.team_2])
                menu.append([
                    InlineMenuButton(text, CallbackId.TS_MATCH_CHOOSE_MATCHUP, callback_data)
                ])
            menu.append([InlineMenuButton('Play with custom teams..', CallbackId.TS_MATCH_CUSTOM_TEAM_OPEN_MENU)])
        menu.append([InlineMenuButton('Cancel', CallbackId.TS_RANKING_OPEN_MENU)])
        return InlineMenu(menu, user_tg_id=context.sender.tg_id)

    @staticmethod
    def _build_quality_markers_string(matchup: TrueSkillMatchup) -> str:
        result = '❤' if matchup.satisfaction >= 0 else '💔'
        if matchup.quality >= 0.50:
            result += '🟢'
        elif matchup.quality > 0.25:
            result += '🟡'
        else:
            result += '🔴'
        result += ' {} {}'.format(round(matchup.quality, 2), round(matchup.win_chance, 2))
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
    def open_menu(context: Context):
        game_session = GameSessionHelpers.get(context)
        if len(PlayerHelpers.get_for_session(context)) < 2:
            Actions.edit_message('Not enough players in session!', message=context.message)
        else:
            Actions.edit_message('Choose your destiny!\nMatch #{}'.format(game_session.matches_played),
                                 message=context.message)
        Actions.edit_markup(MatchmakingHandlers._build_menu_markup(context), message=context.message)

    @staticmethod
    def choose_matchup(context: Context):
        players = PlayerHelpers.get_id_map_for_session(context)
        team_1, team_2 = MatchmakingHandlers._decode_teams(context.message.data)
        menu = InlineMenu([
            [InlineMenuButton(', '.join([players[id].name for id in team_1]), CallbackId.TS_MATCH_CHOOSE_WINNERS,
                              MatchmakingHandlers._encode_teams(team_1, team_2))],
            [InlineMenuButton(', '.join([players[id].name for id in team_2]), CallbackId.TS_MATCH_CHOOSE_WINNERS,
                              MatchmakingHandlers._encode_teams(team_2, team_1))],
            [InlineMenuButton('Back', CallbackId.TS_MATCH_OPEN_MENU)]
        ], user_tg_id=context.sender.tg_id)
        Actions.edit_message('Choose the winners:', message=context.message)
        Actions.edit_markup(menu, message=context.message)

    @staticmethod
    def choose_winners(context: Context):
        team_won, team_lost = MatchmakingHandlers._decode_teams(context.message.data)
        MatchmakingHandlers._update_players(context, team_won, team_lost)
        MatchmakingHandlers.open_menu(context)

    @staticmethod
    def _switch_id_in_list(input: list, element):
        if element in input:
            output = input[:]
            output.remove(element)
            return output
        return input[:] + [element]

    @staticmethod
    def custom_team_open_menu(context: Context, winners_list=None):
        if winners_list is None:
            winners_list = []
        players = PlayerHelpers.get_for_session(context)
        menu = []
        for player in players:
            text = ('✅ {}' if player.id in winners_list else '{}').format(player.name)
            data = MatchmakingHandlers._switch_id_in_list(winners_list, player.id)
            menu.append([
                InlineMenuButton(text, CallbackId.TS_MATCH_CUSTOM_TEAM_CHOOSE_PLAYER, data)
            ])

        menu.append([InlineMenuButton('Confirm', CallbackId.TS_MATCH_CUSTOM_TEAM_CONFIRM, winners_list)])
        menu.append([InlineMenuButton('Cancel', CallbackId.TS_MATCH_OPEN_MENU)])
        Actions.edit_message('Choose your winners:', message=context.message)
        Actions.edit_markup(InlineMenu(menu, user_tg_id=context.sender.tg_id), message=context.message)

    @staticmethod
    def custom_team_choose_player(context: Context):
        winners = [int(x) for x in context.message.data.split()]
        MatchmakingHandlers.custom_team_open_menu(context, winners)

    @staticmethod
    def custom_team_confirm(context: Context):
        team_won = [int(x) for x in context.message.data.split()]
        all_players = PlayerHelpers.get_for_session(context)
        team_lost = [player.id for player in all_players if player.id not in team_won]
        MatchmakingHandlers._update_players(context, team_won, team_lost)
        MatchmakingHandlers.open_menu(context)
