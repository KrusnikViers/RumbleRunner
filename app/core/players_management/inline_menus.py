from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.all import GameRanking, GameSession, Player
from app.routing.callbacks import CallbackIds
from base.api.handler import InlineMenu, InlineMenuButton
from base.api.models import TelegramUser


class MenuConstructor:
    def __init__(self, session: Session, sender: TelegramUser):
        self.session = session
        self.user_tg_id = sender.tg_id

    def players_menu(self, game_ranking: GameRanking) -> InlineMenu:
        menu = list()
        menu.append([InlineMenuButton('Create new player', CallbackIds.TS_NEW_PLAYER)])
        existing_players = self.session.query(Player).filter(Player.game_ranking_id == game_ranking.id).all()
        for player in existing_players:
            menu.append([InlineMenuButton('{}...'.format(player.name), CallbackIds.TS_PLAYER_MENU, player.id)])
        menu.append([InlineMenuButton('Back to rankings', CallbackIds.TS_MAIN_MENU)])
        return InlineMenu(menu, self.user_tg_id)

    @staticmethod
    def player_menu(self, player: Player) -> InlineMenu:
        return InlineMenu([
            [InlineMenuButton('Rename player...', CallbackIds.TS_RENAME_PLAYER, player.id)],
            [
                InlineMenuButton('Reset score', CallbackIds.TS_RESET_SCORE, player.id),
                InlineMenuButton('Delete player', CallbackIds.TS_DELETE_PLAYER, player.id)
            ],
            [InlineMenuButton('Back to players list', CallbackIds.TS_PLAYERS_MENU)]
        ])
