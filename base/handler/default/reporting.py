import logging
import traceback
from typing import Optional

from sqlalchemy.orm import Session
from telegram import Bot, Update

from app.api.config import Config
from base.handler.context.context import Context
from base.models.all import TelegramUser


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
    def report_exception(cls, update: Optional[Update], session: Session):
        message = "Update:\n{}\n\nTraceback:\n{}".format(str(update), traceback.format_exc())
        logging.warning(message)
        superuser = cls._find_superuser(session)
        if superuser:
            cls.instance.bot.send_message(superuser.tg_id, message)

    @classmethod
    def forward_user_message(cls, context: Context):
        superuser = cls._find_superuser(context.session)
        if superuser:
            cls.instance.bot.forward_message(superuser.tg_id,
                                             context.update.effective_chat.id,
                                             context.update.message.message_id)
