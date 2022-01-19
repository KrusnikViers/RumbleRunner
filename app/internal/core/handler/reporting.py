import traceback
from typing import Optional

from telegram import Bot, Update

from app.bot.config import Config
from app.internal.core.handler.context import Context
from app.internal.storage.connection import DatabaseConnection
from app.internal.storage.models.all import TelegramUser
from app.internal.storage.scoped_session import ScopedSession


class ReportsSender:
    # Global instance, being initialized by the main bot class.
    instance = None

    def __init__(self, bot: Bot, configuration: Config):
        self.bot = bot
        self.admin_username = configuration.admin_username

    @classmethod
    def _find_superuser(cls, session) -> Optional[TelegramUser]:
        if cls.instance and cls.instance.admin_username:
            return session.query(TelegramUser).filter_by(username=cls.instance.admin_username).one_or_none()
        return None

    @classmethod
    def report_exception(cls, update: Optional[Update], connection: DatabaseConnection):
        with ScopedSession(connection) as session:
            superuser = cls._find_superuser(session)
            if superuser:
                message = "Update:\n{}\n\nTraceback:\n{}".format(str(update), traceback.format_exc())
                cls.instance.bot.send_message(superuser.tg_id, message)

    @classmethod
    def forward_user_message(cls, context: Context):
        superuser = cls._find_superuser(context.session)
        if superuser:
            cls.instance.bot.forward_message(superuser.tg_id,
                                             context.update.effective_chat.id,
                                             context.update.message.message_id)
