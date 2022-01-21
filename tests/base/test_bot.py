from unittest.mock import MagicMock, patch

import base.bot
from tests.utils import BaseTestCase, MatcherAny


class TestLaunch(BaseTestCase):
    @patch('base.bot.Updater', new=MagicMock())
    @patch('base.bot.DatabaseConnection', new=MagicMock())
    @patch('base.bot.Config', new=MagicMock())
    def test_polling(self):
        bot_instance = base.bot.Bot()
        bot_instance.run()

        bot_instance.updater.start_polling.assert_called_once_with()
        bot_instance.updater.dispatcher.add_handler.assert_called_with(MatcherAny())
        self.assertFalse(bot_instance.updater.start_webhook.called)
