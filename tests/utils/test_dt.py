import os
import sys
import unittest
sys.path.append(os.getcwd())  # NOQA
from app import db, create_app
from config import TestingConfig
from datetime import datetime, timedelta
from app.utils.dt import *


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
        self.assertTrue(is_date_str('2020-02-29'))
        self.assertFalse(is_date_str('2021-02-29'))

    def test_is_time_str(self):
        self.assertTrue(is_time_str('23:59:59'))
        self.assertFalse(is_time_str('23:59:60'))

    def test_is_datetime_str(self):
        self.assertTrue(is_datetime_str('2020-02-29 23:59:59'))
        self.assertFalse(is_datetime_str('2020-02-30 23:59:59'))
        self.assertFalse(is_datetime_str('2020-02-29 23:59:60'))

    def test_date_str_2_datetime(self):
        self.assertEqual(
            datetime(2020, 2, 29),
            date_str_2_datetime('2020-02-29')
        )
        self.assertNotEqual(
            datetime(2020, 2, 28),
            date_str_2_datetime('2020-02-29')
        )

    def test_time_str_2_datetime(self):
        self.assertEqual(
            datetime(2020, 2, 29, 23, 59, 59),
            time_str_2_datetime('23:59:59', dt=datetime(2020, 2, 29))
        )
        self.assertNotEqual(
            datetime(2020, 2, 29, 23, 59, 58),
            time_str_2_datetime('23:59:59', dt=datetime(2020, 2, 29))
        )

    def test_datetime_str_2_datetime(self):
        self.assertEqual(
            datetime(2020, 2, 29, 23, 59, 59),
            datetime_str_2_datetime('2020-02-29 23:59:59')
        )
        self.assertNotEqual(
            datetime(2020, 2, 28, 23, 59, 59),
            datetime_str_2_datetime('2020-02-29 23:59:59')
        )
        self.assertNotEqual(
            datetime(2020, 2, 29, 23, 59, 58),
            datetime_str_2_datetime('2020-02-29 23:59:59')
        )

    def test_second_start(self):
        self.assertEqual(
            datetime(2020, 2, 29, 23, 59, 59),
            second_start(datetime(2020, 2, 29, 23, 59, 59))
        )

    def test_minute_start(self):
        self.assertEqual(
            datetime(2020, 2, 29, 23, 59),
            minute_start(datetime(2020, 2, 29, 23, 59, 59))
        )

    def test_hour_start(self):
        self.assertEqual(
            datetime(2020, 2, 29, 23),
            hour_start(datetime(2020, 2, 29, 23, 59, 59))
        )

    def test_day_start(self):
        self.assertEqual(
            datetime(2020, 2, 29),
            day_start(datetime(2020, 2, 29, 23, 59, 59))
        )

    def test_week_start(self):
        self.assertEqual(0, week_start(datetime.now()).weekday())

    def test_month_start(self):
        self.assertEqual(1, month_start(datetime.now()).day)

    def test_month_end(self):
        self.assertEqual(1, (month_end(datetime.now()) + timedelta(days=1)).day)


if __name__ == '__main__':
    unittest.main(verbosity=2)
