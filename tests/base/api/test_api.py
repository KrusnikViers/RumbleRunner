import glob
import pathlib
from os import path

from app.info import ROOT_DIR
from tests.utils import BaseTestCase


class TestImports(BaseTestCase):
    def test_imports(self):
        modules = glob.glob(str(pathlib.Path(ROOT_DIR).joinpath('base', 'api', '*.py')), recursive=True)
        for file in modules:
            if path.isfile(file) and not file.startswith('_'):
                full_module = 'base.api.{}'.format(path.basename(file)[:-3])
                __import__(full_module, locals(), globals())
