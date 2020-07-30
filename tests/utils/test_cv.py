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

    def test_save_screenshot(self):
        from app.utils import save_screenshot
        # 访问笔记本自带的摄像头
        image_path = save_screenshot(0)
        self.assertTrue(image_path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
