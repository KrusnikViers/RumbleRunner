import logging
import traceback
from typing import Optional

from telegram import Update

from base.database import SessionScope
from base.handler.helpers.actions import Actions
from base.models import TelegramUser


class ReportsSender:
    _admin_username: Optional[str] = None

    @classmethod
    def set_admin(cls, admin_username: Optional[str]):
        cls._admin_username = admin_username

    @classmethod
    def report_exception(cls, update: Optional[Update]):
        message = "Update:\n{}\n\nTraceback:\n{}".format(str(update), traceback.format_exc())
        logging.warning(message)
        superuser = cls._find_superuser()
        if superuser:
            Actions.send_message(message, chat_id=superuser.tg_id)

    @classmethod
    def _find_superuser(cls) -> Optional[TelegramUser]:
        if cls._admin_username:
            return SessionScope.session().query(TelegramUser).filter_by(username=cls._admin_username).one_or_none()
        return None
