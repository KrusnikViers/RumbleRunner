from app.internal.core.handler.context import Context
from app.internal.core.handler.memberhsip import update_memberships


def default_processing(context: Context):
    update_memberships(context)
