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

    def test_check_rtsp(self):
        from app.utils import check_rtsp
        self.assertTrue(check_rtsp('rtsp://192.168.1.2'))
        self.assertTrue(check_rtsp('rtsp://admin:123456@192.168.1.2'))
        self.assertFalse(check_rtsp('http://192.168.1.2'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
