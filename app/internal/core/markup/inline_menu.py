from typing import Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.internal.core.markup.callback_commands import encode_callback_data, CallbackData


class InlineMenu(InlineKeyboardMarkup):
    # Expects a list of rows, where each row is a list of tuples ('Button text', [command, <parameters>])
    # If close_button_text not empty, adds button with "CANCEL" action attached
    # user_id should be provided for menu to work as personal callback.
    def __init__(self, markup: list, user_tg_id: Optional[int] = ''):
        super(InlineMenu, self).__init__(
            [[InlineKeyboardButton(text,
                                   callback_data=encode_callback_data(CallbackData(data[0], user_tg_id, data[1:])))
              for text, data in row] for row in markup])
