import logging
from typing import Optional

from telegram.ext import Updater

from app.api import Config
from app.api.routing_list import ROUTING_LIST
from base import DatabaseConnection, ReportsSender
from base.handler.helpers.actions import BotScope
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

        self.configuration = Config.parse()
        self.updater = Updater(token=self.configuration.bot_token)
        self.database_connection = DatabaseConnection.create(self.configuration.storage_dir)
        self.dispatcher = Dispatcher(self.updater, self.database_connection, ROUTING_LIST)
        ReportsSender.set_admin(self.configuration.admin_username)

        logging.info('Launching bot: ' + str(self.updater.bot.get_me()))
        with BotScope(self.updater.bot):
            self.updater.start_polling()
            # This call will lock execution until worker threads are stopped with SIGINT(2), SIGTERM(15) or SIGABRT(6).
            self.updater.idle()
