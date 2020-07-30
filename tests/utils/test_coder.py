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

    def test_base64(self):
        from app.utils import Base64Coder
        self.assertEqual('aGVsbG8=\n', Base64Coder().encode('hello'))
        self.assertEqual('hello', Base64Coder().decode(Base64Coder().encode('hello')))

    def test_hash(self):
        from app.utils import HashCoder
        self.assertEqual('5d41402abc4b2a76b9719d911017c592', HashCoder().encode('hello'))

    def test_hmac(self):
        from app.utils import HmacCoder
        self.assertEqual('8a64982d1ed45b361c80a14aa2cad9a8', HmacCoder(key='hh', msg='kk').encode('hello'))

    def test_aes(self):
        from app.utils import AESCoder
        token = AESCoder('hellohellohelloo').encode('hello')
        self.assertEqual('5bd2d16dbb2937a20652f873c73c1dcd', token)
        self.assertEqual('hello', AESCoder('hellohellohelloo').decode(token))

    def test_rsa(self):
        from app.utils import RSACoder
        rsa = RSACoder()
        token = rsa.encode('hello')
        self.assertEqual('hello', rsa.decode(token))

    def test_jwt(self):
        from app.utils import JWTCoder
        token = JWTCoder('hello').encode({'hello': 'world'})
        self.assertEqual({'hello': 'world'}, JWTCoder('hello').decode(token))

    def test_generate_random_string(self):
        from app.utils import generate_random_string
        self.assertRegex(generate_random_string(16), r'[a-zA-Z]{16}')
        self.assertRegex(generate_random_string(16, digits=True), r'[a-zA-Z0-9]{16}')


if __name__ == '__main__':
    unittest.main(verbosity=2)
