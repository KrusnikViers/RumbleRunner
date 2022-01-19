from app.bot.routing.callbacks import CallbackIds
from tests.base import BaseTestCase


class TestCallbacks(BaseTestCase):
    def test_callback_ids_unique(self):
        ids_dict = dict()
        for name, value in vars(CallbackIds).items():
            if isinstance(value, int):
                if value in ids_dict:
                    ids_dict[value].append(name)
                else:
                    ids_dict[value] = [name]
        for value, names in ids_dict.items():
            self.assertEqual(len(names), 1, "Duplicate names: {}".format(', '.join(names)))
