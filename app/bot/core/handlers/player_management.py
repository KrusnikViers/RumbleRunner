from typing import Optional

from telegram import TelegramError

from app.bot.core.rankings.trueskill import DEFAULT_MU, DEFAULT_SIGMA
from app.bot.models.all import Player
from app.bot.routing.callbacks import CallbackIds
from app.public.handlers import Context
from app.public.markup import InlineMenu, decode_callback_data


def create_player(context: Context):
    arguments = context.command_argument()
    if len(arguments) == 0 or len(arguments.split()) != 1:
        context.send_response_message("Usage: /create_player Player_name_no_spaces")
        return
    new_player_name = arguments
    existing_player = context.session.query(Player).filter(Player.name == new_player_name).one_or_none()
    if existing_player is not None:
        context.send_response_message("Player {} already exists".format(new_player_name))
        return
    context.session.add(Player(name=new_player_name, mu=DEFAULT_MU, sigma=DEFAULT_SIGMA))
    context.send_response_message("Player {} created!".format(new_player_name))


def _delete_player_markup(context: Context) -> Optional[InlineMenu]:
    all_players = context.session.query(Player).all()
    if len(all_players) == 0:
        return None
    player_rows = [[('Remove {}'.format(player.name), [CallbackIds.PM_DELETE_PLAYER, player.id])]
                   for player in all_players]
    return InlineMenu(player_rows + [[('Cancel', [CallbackIds.COMMON_CANCEL_DELETE_MESSAGE_PERSONAL])]],
                      user_tg_id=context.sender.tg_id)


def delete_player(context: Context):
    markup = _delete_player_markup(context)
    if markup is None:
        context.send_response_message("No players to be deleted")
    else:
        context.send_response_message("Select players to be deleted\nCan not be undone!", reply_markup=markup)


def delete_player_callback(context: Context):
    player_id = decode_callback_data(context.update).data[0]
    player = context.session.query(Player).filter(Player.id == player_id).one_or_none()
    if player:
        context.session.delete(player)
        context.session.commit()
    new_markup = _delete_player_markup(context)
    try:
        if new_markup is None:
            context.update.callback_query.edit_message_text("No more players to be deleted")
            context.update.callback_query.edit_message_reply_markup(None)
        else:
            context.update.callback_query.edit_message_reply_markup(new_markup)
    except TelegramError:
        pass
    context.update.callback_query.answer()
