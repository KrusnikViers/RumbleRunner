from tests.base import BaseTestCase
from app.bot.info import APP_DIR

import pathlib
import glob
from os import path

class TestImports(BaseTestCase):
    def test_imports(self):
        modules = glob.glob(str(pathlib.Path(APP_DIR).joinpath('public', '*.py')), recursive=True)
        for file in modules:
            if path.isfile(file) and not file.startswith('_'):
                full_module = 'app.public.{}'.format(path.basename(file)[:-3])
                __import__(full_module, locals(), globals())
