from app.models.all import GameRanking
from base.api.handler import Context


class GameRankingEntity:
    @staticmethod
    def get_or_create(context: Context) -> GameRanking:
        game_ranking = context.session.query(GameRanking).filter(
            GameRanking.tg_group_id == context.group.tg_id).one_or_none()
        if game_ranking is None:
            game_ranking = GameRanking(tg_group_id=context.group.tg_id)
            context.session.add(game_ranking)
            context.session.commit()
        return game_ranking
