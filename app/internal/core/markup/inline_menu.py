from typing import Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.internal.core.markup.callback_commands import encode_callback_data


class InlineMenu(InlineKeyboardMarkup):
    # Expects a list of rows, where each row is a list of tuples ('Button text', [command, <parameters>])
    # If close_button_text not empty, adds button with "CANCEL" action attached
    # user_id should be provided for menu to work as personal callback.
    def __init__(self, markup: list, user_tg_id: Optional[int] = None):
        if user_tg_id is not None:
            self._insert_user_id(markup, user_tg_id)
        super(InlineMenu, self).__init__([[InlineKeyboardButton(text, callback_data=encode_callback_data(data))
                                           for text, data in row] for row in markup])

    @staticmethod
    def _insert_user_id(markup: list, user_id: int):
        for row in markup:
            for text, data in row:
                data.insert(1, user_id)
