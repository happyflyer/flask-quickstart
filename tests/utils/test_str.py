# -*- coding: utf-8 -*-

import os
import sys
import unittest
sys.path.append(os.getcwd())  # NOQA

from app import db, create_app
from config import TestingConfig


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
        from app.utils import has_empty
        self.assertFalse(has_empty('hh', 'kk'))
        self.assertTrue(has_empty('hh', 'kk', '   '))

    def test_all_empty(self):
        from app.utils import all_empty
        self.assertFalse(all_empty('hh', 'kk', '   '))
        self.assertTrue(all_empty('  ', '', '   '))


if __name__ == '__main__':
    unittest.main(verbosity=2)
