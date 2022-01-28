from typing import Optional

from telegram import Bot


class BotScope:
    _bot: Optional[Bot] = None

    @classmethod
    def bot(cls) -> Bot:
        assert cls._bot is not None
        return cls._bot

    def __init__(self, bot: Bot):
        self.old_value = None
        self.bot = bot

    def __enter__(self):
        self.old_value = BotScope._bot
        BotScope._bot = self.bot

    def __exit__(self, exc_type, exc_val, exc_tb):
        BotScope._bot = self.old_value
