from base.handler.wrappers import Context, Requests


def delete_message(context: Context):
    context.delete_message()


def delete_message_and_pending_request(context: Context):
    Requests.delete(context)
    delete_message(context)
