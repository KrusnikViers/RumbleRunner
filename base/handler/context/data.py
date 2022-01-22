from typing import Optional, Union

from telegram import Update


class CallbackData:
    def __init__(self, command: int, user_id: Optional[int] = None, data: Union[None, str, list] = None):
        self.command = command
        self.user_id = user_id
        self.data = ' '.join([str(x) for x in data]) if isinstance(data, list) else data

    @staticmethod
    def parse(raw_callback_data: str):
        data_split = raw_callback_data.split(':', maxsplit=3)
        return CallbackData(
            int(data_split[0]),
            int(data_split[1]) if data_split[1] else None,
            data_split[2] if data_split[2] else None
        )

    def encode(self):
        def empty_if_none(x): return '' if x is None else x
        return '{0}:{1}:{2}'.format(int(self.command), str(empty_if_none(self.user_id)), empty_if_none(self.data))


class Data:
    def __init__(self, update: Update):
        self.update: Update = update

        self.is_empty: bool = True
        self.bot_command: Optional[str] = None
        self.text: Optional[str] = None
        self.callback_data: Optional[CallbackData] = None

        self._parse_message()
        self._parse_callback_data()

    def _parse_message(self):
        if self.update.effective_message is None:
            return
        text = self.update.effective_message.text
        if not text:
            return
        # Bot command
        if text.startswith('/'):
            divider = text.find(' ')
            # Empty command
            if divider == -1:
                self.bot_command = text.strip()
                return
            # Command with argument
            else:
                self.bot_command = text[:divider].strip()
                self.text = text[divider + 1:].strip()
                self.is_empty = False
        # Usual message
        else:
            self.text = text.strip()
            self.is_empty = False

    def _parse_callback_data(self):
        if self.update.callback_query is None or self.update.callback_query.data is None:
            return
        self.callback_data = CallbackData.parse(self.update.callback_query.data)
        self.is_empty = False
