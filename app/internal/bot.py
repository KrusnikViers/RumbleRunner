import logging
from typing import Optional

from telegram.ext import Updater

from app.bot.config import Config
from app.bot.routing.handlers import HANDLERS as GENERAL_HANDLERS
from app.bot.routing.pending_requests import HANDLERS as PENDING_REQUESTS_HANDLERS
from app.internal.core.dispatcher import Dispatcher
from app.internal.log import global_logging_init
from app.internal.storage.connection import DatabaseConnection


class Bot:
    def __init__(self):
        self.updater: Optional[Updater] = None
        self.configuration: Optional[Config] = None
        self.database_connection: Optional[DatabaseConnection] = None
        self.dispatcher: Optional[Dispatcher] = None

    def run(self):
        global_logging_init()

        self.configuration = Config.get()
        self.updater = Updater(token=self.configuration.bot_token)
        self.database_connection = DatabaseConnection(self.configuration)
        self.dispatcher = Dispatcher(self.updater, self.database_connection,
                                     GENERAL_HANDLERS, PENDING_REQUESTS_HANDLERS)
        # ReportsSender.instance = ReportsSender(self.updater.bot, self.configuration) TODO

        logging.info('Launching bot: ' + str(self.updater.bot.get_me()))
        self.updater.start_polling()
        # This call will lock execution until worker threads are stopped with SIGINT(2), SIGTERM(15) or SIGABRT(6).
        self.updater.idle()
