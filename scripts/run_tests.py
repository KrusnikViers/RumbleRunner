import os
import pathlib
import unittest


project_directory = pathlib.Path(os.path.realpath(__file__)).parent.parent
tests_list = unittest.TestLoader().discover(str(project_directory))
unittest.TextTestRunner().run(tests_list)
