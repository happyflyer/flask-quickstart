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

    def test_read_json(self):
        from app.utils import read_json
        payload = read_json('tests/data/demo.json')
        self.assertIn('a', payload)
        self.assertEqual({'a': 'b'}, payload)

    def test_write_json(self):
        from app.utils import write_json
        write_json({'a': 'b'}, 'tests/data/demo.json')
        self.assertTrue(os.path.exists('tests/data/demo.json'))

    def test_read_properties(self):
        from app.utils import read_properties
        payload = read_properties('tests/data/demo.properties')
        self.assertIn('a', payload)
        self.assertIn('b', payload.get('a'))
        self.assertIn('d', payload.get('a').get('c'))
        self.assertIn('h', payload.get('a').get('e').get('f').get('g'))
        self.assertEqual(
            {'a': {'b': '1', 'c': {'d': '3'}, 'e': {'f': {'g': {'h': '4'}}}}, 'x': '5', 'y': {'z': '6'}},
            payload)


if __name__ == '__main__':
    unittest.main(verbosity=2)
