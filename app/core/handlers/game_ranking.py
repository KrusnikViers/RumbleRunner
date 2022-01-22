from app.core.handlers.inline_menus import MenuConstructor
from app.models.game_ranking import GameRanking
from base.api.handler import Context


def main_menu(context: Context):
    game_ranking = context.session.query(GameRanking).filter(
        GameRanking.tg_group_id == context.group.tg_id).one_or_none()
    if game_ranking is None:
        game_ranking = GameRanking(tg_group_id=context.group.tg_id)
        context.session.add(game_ranking)
        context.session.commit()

    menu = MenuConstructor(context.session, context.sender)
    context.actions.send_message('Game Rankings', reply_markup=menu.main_menu(game_ranking))


def main_menu_callback(context: Context):
    game_ranking = context.session.query(GameRanking).filter(
        GameRanking.tg_group_id == context.group.tg_id).first()
    menu = MenuConstructor(context.session, context.sender)
    context.actions.edit_markup(menu.main_menu(game_ranking))
