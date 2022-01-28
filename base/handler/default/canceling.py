from base.api.handler import Context
from base.handler.helpers.actions import Actions
from base.handler.wrappers.requests import Requests


def delete_message(context: Context):
    Actions.delete_message(message=context.message)


def delete_message_and_pending_request(context: Context):
    Requests.delete(context)
    delete_message(context)
