from telegram import Update


def encode_callback_data(data: list) -> str:
    return ' '.join([str(x) for x in data])


def decode_callback_data(update: Update) -> tuple:
    return tuple(update.callback_query.data.split())
