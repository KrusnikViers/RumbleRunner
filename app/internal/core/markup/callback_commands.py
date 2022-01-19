from collections import namedtuple

from telegram import Update

CallbackData = namedtuple('CallbackData', 'command user_id data')


def encode_callback_data(data: CallbackData) -> str:
    return "{0}:{1}:{2}".format(str(data.command), str(data.user_id), ' '.join([str(x) for x in data.data]))


def decode_callback_data(update: Update) -> CallbackData:
    data = update.callback_query.data.split(':', maxsplit=3)
    command = data[0]
    user_id = data[1]
    general_data = data[2].split()
    return CallbackData(command, user_id, general_data)
