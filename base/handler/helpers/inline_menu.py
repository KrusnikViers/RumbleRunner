from typing import Optional, List, Union

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from base.handler.context.data import CallbackData


class InlineMenuButton:
    def __init__(self, text: str, command: int, callback_data: Union[str, list, None] = None):
        self.text = text
        self.command = command
        self.callback_data = callback_data


class InlineMenu(InlineKeyboardMarkup):
    # List of rows, each row may have multiple columns in it. If |user_tg_id| is provided, menu for personal callbacks
    # will be generated.
    def __init__(self, markup: List[List[InlineMenuButton]], user_tg_id: Optional[int] = None):
        super(InlineMenu, self).__init__(
            [[InlineMenu._button_markup(button, user_tg_id) for button in row] for row in markup])

    @staticmethod
    def _button_markup(button: InlineMenuButton, user_tg_id: Optional[int]):
        return InlineKeyboardButton(button.text, callback_data=CallbackData(button.command, user_tg_id,
                                                                            button.callback_data).encode())
