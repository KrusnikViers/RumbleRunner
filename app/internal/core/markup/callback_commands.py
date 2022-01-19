from telegram import Update


def encode_callback_data(data: list) -> str:
    return ' '.join([str(x) for x in data])


def decode_callback_data(update: Update, is_personal=False) -> tuple:
    offset = 2 if is_personal else 1
    data_split = update.callback_query.data.split()
    return tuple(update.callback_query.data.split()[offset:]) if len(data_split) > offset else []
