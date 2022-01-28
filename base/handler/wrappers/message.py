from typing import Optional, Union

from telegram import Update, Message as TgMessage

from app import CallbackId, value_to_enum


class CallbackData:
    def __init__(self, command: int, user_id: Optional[int] = None, data: Union[None, str, list] = None):
        self.command = command
        self.user_id = user_id
        self.data = ' '.join([str(x) for x in data]) if isinstance(data, list) else data

    @staticmethod
    def parse(raw_callback_data: str):
        data_split = raw_callback_data.split(':', maxsplit=3)
        return CallbackData(
            CallbackId(int(data_split[0])),
            int(data_split[1]) if data_split[1] else None,
            data_split[2] if data_split[2] else None
        )

    def encode(self):
        def empty_if_none(x):
            return '' if x is None else x

        return '{0}:{1}:{2}'.format(int(self.command), str(empty_if_none(self.user_id)), empty_if_none(self.data))


class Message:
    def __init__(self, command: Union[str, CallbackId, None] = None, data: Optional[str] = None,
                 chat_id=None, message_id=None, callback_user_id=None):
        self.command: Union[str, CallbackId, None] = command
        self.data: Optional[str] = data

        self.chat_id: Optional[int] = chat_id
        self.message_id: Optional[int] = message_id

        self.callback_user_id: Optional[int] = callback_user_id

    @classmethod
    def from_update(cls, update: Update) -> Optional['Message']:
        if update.callback_query is not None:
            return cls._from_callback(update)
        elif update.effective_message is not None:
            return cls._from_message(update)
        return None

    # Private methods:
    @classmethod
    def _from_callback(cls, update: Update) -> Optional['Message']:
        if not update.callback_query.data:
            return None
        callback_data = CallbackData.parse(update.callback_query.data)
        chat_id, message_id = Message._parse_ids(update.callback_query.message)
        return cls(value_to_enum(CallbackId, callback_data.command), callback_data.data,
                   callback_user_id=callback_data.user_id, chat_id=chat_id, message_id=message_id)

    @classmethod
    def _from_message(cls, update: Update) -> 'Message':
        command, data = Message._parse_message_text(update.effective_message.text)
        chat_id, message_id = Message._parse_ids(update.effective_message)
        return cls(command, data, chat_id=chat_id, message_id=message_id)

    @staticmethod
    def _parse_message_text(text: str) -> (Optional[str], Optional[str]):
        if not text:
            return None, None
        # Usual message
        if not text.startswith('/'):
            return None, text.strip()
        elif text.find(' ') == -1:
            return text.strip(), None
        else:
            divider = text.find(' ')
            return text[:divider].strip(), text[divider + 1:].strip()

    @staticmethod
    def _parse_ids(message: TgMessage) -> (Optional[int], Optional[int]):
        return message.chat_id, message.message_id
