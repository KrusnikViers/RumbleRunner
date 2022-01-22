from base.api.handler import Context
from base.api.routing import PendingRequests


def delete_message(context: Context):
    context.actions.delete_message()


def delete_message_and_pending_request(context: Context):
    pending_request = PendingRequests.get(context)
    if pending_request:
        context.session.delete(pending_request)
        context.session.commit()
    delete_message(context)
