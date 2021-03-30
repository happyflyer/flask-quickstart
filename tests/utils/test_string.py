import os
import sys
import unittest
sys.path.append(os.getcwd())  # NOQA
from app import db, create_app
from config import TestingConfig
from app.utils.string import *


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_has_empty(self):
        self.assertFalse(has_empty('hh', 'kk'))
        self.assertTrue(has_empty('hh', 'kk', '   '))

    def test_all_empty(self):
        self.assertFalse(all_empty('hh', 'kk', '   '))
        self.assertTrue(all_empty('  ', '', '   '))

    def test_is_empty(self):
        self.assertTrue(is_empty(''))
        self.assertTrue(is_empty('  '))
        self.assertFalse(is_empty('h'))
        self.assertFalse(is_empty(0))
        self.assertFalse(is_empty(1))
        self.assertTrue(is_empty(()))
        self.assertTrue(is_empty([]))
        self.assertTrue(is_empty({}))


if __name__ == '__main__':
    unittest.main(verbosity=2)
