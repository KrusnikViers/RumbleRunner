from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class InlineMenu(InlineKeyboardMarkup):
    # Expects a list of rows, where each row is a list of tuples ('Button text', [command, <parameters>])
    # If close_button_text not empty, adds button with "CANCEL" action attached
    # user_id should be provided for menu to work as personal callback.
    def __init__(self, markup: list, user_id: int = None):
        if user_id is not None:
            self._insert_user_id(markup, user_id)

        def encode(data):
            return ' '.join([str(x) for x in data])

        super(InlineMenu, self).__init__([[InlineKeyboardButton(text, callback_data=encode(data))
                                           for text, data in row] for row in markup])

    @staticmethod
    def _insert_user_id(markup: list, user_id: int):
        for row in markup:
            for text, data in row:
                data.insert(1, user_id)
