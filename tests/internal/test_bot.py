from unittest.mock import MagicMock, patch

import app.internal.bot
from tests.base import BaseTestCase, MatcherAny


class TestLaunch(BaseTestCase):
    @patch('app.internal.bot.Updater', new=MagicMock())
    @patch('app.internal.bot.DatabaseConnection', new=MagicMock())
    @patch('app.internal.bot.Config', new=MagicMock())
    def test_polling(self):
        bot_instance = app.internal.bot.Bot()
        bot_instance.run()

        bot_instance.updater.start_polling.assert_called_once_with()
        bot_instance.updater.dispatcher.add_handler.assert_called_with(MatcherAny())
        self.assertFalse(bot_instance.updater.start_webhook.called)
