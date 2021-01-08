import os
import sys
import unittest
sys.path.append(os.getcwd())  # NOQA
from app import db, create_app
from config import TestingConfig
from app.utils.io import *


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

    def test_read_json(self):
        write_json({'a': 'b'}, 'tmp/tests/utils/demo.json', new_thread=False)
        payload = read_json('tmp/tests/utils/demo.json')
        self.assertIn('a', payload)
        self.assertEqual({'a': 'b'}, payload)

    def test_write_json(self):
        write_json({'a': 'b'}, 'tmp/tests/utils/demo.json')
        self.assertTrue(os.path.exists('tmp/tests/utils/demo.json'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
