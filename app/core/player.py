from typing import List, Optional, Dict

from app.core.game_ranking import GameRankingHelpers
from app.core.game_session import GameSessionHelpers
from app.models import Player
from base import SessionScope, Context


class PlayerHelpers:
    @staticmethod
    def by_id(id) -> Optional[Player]:
        return SessionScope.session().query(Player).filter(Player.id == id).one_or_none()

    @staticmethod
    def get_for_ranking(context: Context) -> List[Player]:
        game_ranking = GameRankingHelpers.get_or_create(context)
        players = SessionScope.session().query(Player).filter(Player.game_ranking_id == game_ranking.id).all()
        return sorted(players, key=PlayerHelpers.sorting_key)

    @staticmethod
    def get_for_session(context: Context):
        current_session = GameSessionHelpers.get(context)
        return SessionScope.session().query(Player).filter(Player.game_session_id == current_session.id).all()

    @staticmethod
    def get_id_map_for_session(context: Context) -> Dict[int, Player]:
        players = PlayerHelpers.get_for_session(context)
        return {player.id: player for player in players}

    @staticmethod
    def sorting_key(player: Player):
        return player.sigma, player.id
