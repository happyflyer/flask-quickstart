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

    def test_is_date_str(self):
        from app.utils import is_date_str
        self.assertTrue(is_date_str('2020-02-29'))
        self.assertFalse(is_date_str('2021-02-29'))

    def test_is_time_str(self):
        from app.utils import is_time_str
        self.assertTrue(is_time_str('23:59:59'))
        self.assertFalse(is_time_str('10:01:60'))

    def test_date_str_2_dt(self):
        from datetime import datetime
        from app.utils import date_str_2_dt
        self.assertEqual(datetime(2020, 1, 1, 0, 0, 0), date_str_2_dt('2020-01-01'))

    def test_time_str_2_dt(self):
        from datetime import datetime
        from app.utils import time_str_2_dt
        self.assertEqual(datetime(2020, 12, 31, 23, 59, 59),
            time_str_2_dt('23:59:59', dt=datetime(2020, 12, 31)))  # NOQA

    def test_dt_str_2_dt(self):
        from datetime import datetime
        from app.utils import dt_str_2_dt
        self.assertEqual(datetime(2020, 12, 31, 23, 59, 59), dt_str_2_dt('2020-12-31 23:59:59'))

    def test_dt_start(self):
        from datetime import datetime
        from app.utils import dt_start
        self.assertEqual(datetime(2020, 12, 31), dt_start(datetime(2020, 12, 31, 23, 59, 59)))

    def test_dt_end(self):
        from datetime import datetime
        from app.utils import dt_end
        self.assertEqual(datetime(2020, 12, 31, 23, 59, 59), dt_end(datetime(2020, 12, 31)))

    def test_get_monday(self):
        from datetime import datetime
        from app.utils import get_monday
        self.assertEqual(0, get_monday(datetime.now()).weekday())

    def test_get_sunday(self):
        from datetime import datetime
        from app.utils import get_sunday
        self.assertEqual(6, get_sunday(datetime.now()).weekday())

    def test_get_firstday(self):
        from datetime import datetime
        from app.utils import get_firstday
        self.assertEqual(1, get_firstday(datetime.now()).day)

    def test_get_lastday(self):
        from datetime import datetime, timedelta
        from app.utils import get_lastday
        self.assertEqual(1, (get_lastday(datetime.now()) + timedelta(days=1)).day)


if __name__ == '__main__':
    unittest.main(verbosity=2)
