from typing import List

from app.api import CallbackId
from app.core import GameSessionHelpers, PlayerHelpers, TrueSkillMatchup, TrueSkillClient
from app.models import Participation
from base import SessionScope, Context, InlineMenuButton


class MatchupSelectionHandlers:
    _MARKS = {
        'star': '⭐', 'glowing_star': '🌟',
        'heart': '❤', 'broken_heart': '💔',
        'green': '🟢', 'yellow': '🟡', 'orange': '🟠', 'red': '🔴'
    }

    @staticmethod
    def _get_matchups(context):
        return TrueSkillClient.select_good_matchups(context)[:8]

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
    def _matchup_marks(matchup: TrueSkillMatchup):
        result = ''
        if matchup.streakbreaker > 0:
            result += MatchupSelectionHandlers._MARKS['heart']
        elif matchup.streakbreaker < 0:
            result += MatchupSelectionHandlers._MARKS['broken_heart']
        if matchup.uncertainty >= 0.5 and abs(matchup.win_chance - 0.5) < 0.2:
            result += MatchupSelectionHandlers._MARKS['green']
        elif matchup.uncertainty >= 0.5 or abs(matchup.win_chance - 0.5) < 0.2:
            result += MatchupSelectionHandlers._MARKS['yellow']
        elif matchup.uncertainty >= 0.2 and abs(matchup.win_chance - 0.5) < 0.2:
            result += MatchupSelectionHandlers._MARKS['orange']
        else:
            result += MatchupSelectionHandlers._MARKS['red']
        return result

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
    def _title(context: Context, matchups: List[TrueSkillMatchup]):
        players_map = PlayerHelpers.get_id_map_for_session(context)
        matchup_descriptions = []
        for index, matchup in enumerate(matchups):
            matchup_descriptions.append(
                ("Option {} {}\n"
                 "{}\n"
                 "{}"
                 ).format(str(index + 1),
                          MatchupSelectionHandlers._matchup_marks(matchup),
                          ", ".join([players_map[player.id].name for player in matchup.team_1]),
                          ", ".join([players_map[player.id].name for player in matchup.team_2])))
        return "Choose your matchup:\n\n" + "\n\n".join(matchup_descriptions)

    @staticmethod
    def _markup(context: Context, matchups: List[TrueSkillMatchup]):
        menu = [[]]
        for index, matchup in enumerate(matchups):
            team_1 = [x.id for x in matchup.team_1]
            team_2 = [x.id for x in matchup.team_2]
            menu[0].append(InlineMenuButton('#{}'.format(index + 1), CallbackId.MATCHUP_SELECTION_CHOOSE_MATCHUP,
                                            MatchupSelectionHandlers._encode_teams(team_1, team_2)))
        menu.append([InlineMenuButton('Custom teams', CallbackId.MATCHUP_SELECTION_CUSTOM_WINNERS_REDRAW)])
        menu.append([InlineMenuButton('Back', CallbackId.MAIN_MENU_OPEN)])
        return context.personal_menu(menu)

    @staticmethod
    def open(context: Context):
        if context.message.is_callback:
            context.delete_message()
        matchups = MatchupSelectionHandlers._get_matchups(context)
        context.send_message(MatchupSelectionHandlers._title(context, matchups),
                             reply_markup=MatchupSelectionHandlers._markup(context, matchups))

    @staticmethod
    def redraw(context: Context):
        matchups = MatchupSelectionHandlers._get_matchups(context)
        context.edit_message(MatchupSelectionHandlers._title(context, matchups),
                             reply_markup=MatchupSelectionHandlers._markup(context, matchups))

    @staticmethod
    def choose_matchup(context: Context):
        team1, team2 = MatchupSelectionHandlers._decode_teams(context.message.data)
        players_map = PlayerHelpers.get_id_map_for_session(context)
        title = 'This time, winners are:'
        markup = context.personal_menu([
            [
                InlineMenuButton(", ".join([players_map[player_id].name for player_id in team1]),
                                 CallbackId.MATCHUP_SELECTION_CHOOSE_WINNER_TEAM,
                                 MatchupSelectionHandlers._encode_teams(team1, team2)),
                InlineMenuButton(", ".join([players_map[player_id].name for player_id in team2]),
                                 CallbackId.MATCHUP_SELECTION_CHOOSE_WINNER_TEAM,
                                 MatchupSelectionHandlers._encode_teams(team2, team1))
            ],
            [InlineMenuButton("Cancel", CallbackId.MATCHUP_SELECTION_OPEN)]
        ])
        context.delete_message()
        context.send_message(title, reply_markup=markup)

    @staticmethod
    def choose_winner_team(context: Context):
        team_won, team_lost = MatchupSelectionHandlers._decode_teams(context.message.data)
        MatchupSelectionHandlers._update_players(context, team_won, team_lost)
        MatchupSelectionHandlers.open(context)

    @staticmethod
    def _switch_id_in_list(input: list, element):
        if element in input:
            output = input[:]
            output.remove(element)
            return output
        return input[:] + [element]

    @staticmethod
    def custom_winners_redraw(context: Context, winners_list=None):
        if winners_list is None:
            winners_list = []
        players = PlayerHelpers.get_for_session(context)
        menu = []
        for player in players:
            text = ('✅ {}' if player.id in winners_list else '{}').format(player.name)
            data = MatchupSelectionHandlers._switch_id_in_list(winners_list, player.id)
            menu.append([
                InlineMenuButton(text, CallbackId.MATCHUP_SELECTION_CUSTOM_WINNERS_SWITCH, data)
            ])
        menu.append([InlineMenuButton('Confirm', CallbackId.MATCHUP_SELECTION_CUSTOM_WINNERS_CONFIRM, winners_list)])
        menu.append([InlineMenuButton('Cancel', CallbackId.MATCHUP_SELECTION_OPEN)])
        context.edit_message('Choose players who won custom match:', reply_markup=context.personal_menu(menu))

    @staticmethod
    def custom_winners_switch(context: Context):
        winners = [int(x) for x in context.message.data.split()]
        MatchupSelectionHandlers.custom_winners_redraw(context, winners)

    @staticmethod
    def custom_winners_confirm(context: Context):
        team_won = [int(x) for x in context.message.data.split()]
        all_players = PlayerHelpers.get_for_session(context)
        team_lost = [player.id for player in all_players if player.id not in team_won]
        MatchupSelectionHandlers._update_players(context, team_won, team_lost)
        MatchupSelectionHandlers.open(context)
