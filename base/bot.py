import logging
from typing import Optional

from telegram.ext import Updater

from app.config import Config
from app.routing.dispatcher import UPDATE_HANDLERS
from app.routing.pending_requests import PENDING_REQUESTS_HANDLERS
from base.api.database import DatabaseConnection
from base.handler.default.reporting import ReportsSender
from base.routing.dispatcher import Dispatcher


class Bot:
    def __init__(self):
        self.updater: Optional[Updater] = None
        self.configuration: Optional[Config] = None
        self.database_connection: Optional[DatabaseConnection] = None
        self.dispatcher: Optional[Dispatcher] = None

    @staticmethod
    def set_logging_format():
        logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - %(message)s', level=logging.INFO)

    def run(self):
        Bot.set_logging_format()

        self.configuration = Config.get()
        self.updater = Updater(token=self.configuration.bot_token)
        self.database_connection = DatabaseConnection(self.configuration)
        self.dispatcher = Dispatcher(self.updater, self.database_connection,
                                     UPDATE_HANDLERS, PENDING_REQUESTS_HANDLERS)
        ReportsSender.instance = ReportsSender(self.updater.bot, self.configuration)

        logging.info('Launching bot: ' + str(self.updater.bot.get_me()))
        self.updater.start_polling()
        # This call will lock execution until worker threads are stopped with SIGINT(2), SIGTERM(15) or SIGABRT(6).
        self.updater.idle()
