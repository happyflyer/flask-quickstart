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

    def test_get_os(self):
        from app.utils import get_os
        self.assertIn(get_os(), ['Windows', 'Linux', 'Darwin'])

    def test_get_ip(self):
        from app.utils import get_ip
        self.assertIsInstance(get_ip(), list)

    def test_check_ip(self):
        from app.utils import check_ip
        self.assertTrue(check_ip('192.168.1.1'))
        self.assertFalse(check_ip('192.168.1.256'))

    def test_extract_ip(self):
        from app.utils import extract_ip
        self.assertEqual('192.168.1.1', extract_ip('gate is 192.168.1.1, and my ip address is 192.168.1.4'))

    def test_ping_ip(self):
        from app.utils import ping_ip
        self.assertTrue(ping_ip('127.0.0.1'))

    def test_scan_ip(self):
        from app.utils import scan_ip
        self.assertIsInstance(scan_ip('192.168.1.1'), list)


if __name__ == '__main__':
    unittest.main(verbosity=2)
