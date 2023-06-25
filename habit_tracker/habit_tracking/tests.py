
# Create your tests here.
import unittest

from .helping_function import get_days_difference


class TestGetDaysDifference(unittest.TestCase):
    def test_days_difference(self):
        # Test case 1: date2 is later than date1
        date1 = '10/15/2022'
        date2 = '12/31/2022'
        self.assertEqual(get_days_difference(date1, date2), 77)

        # Test case 2: date1 is later than date2
        date1 = '12/31/2022'
        date2 = '10/15/2022'
        self.assertEqual(get_days_difference(date1, date2), -77)

        # Test case 3: date1 and date2 are the same
        date1 = '01/01/2023'
        date2 = '01/01/2023'
        self.assertEqual(get_days_difference(date1, date2), 0)

        # Test case 4: date1 and date2 are exactly one year apart (including a leap year)
        date1 = '01/01/2023'
        date2 = '01/01/2024'
        self.assertEqual(get_days_difference(date1, date2), 366)

# Create your tests here.
