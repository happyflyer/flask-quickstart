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


if __name__ == '__main__':
    unittest.main(verbosity=2)
