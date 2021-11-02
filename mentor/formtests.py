from typing import Type
import unittest

from utils import create_day_array

class TestFormCreation(unittest.TestCase):
    """Tests functions within create_user_form."""

    def test_day_array(self):
        """Testing the create_day_array function. This is normally called
        in the profile creation form to turn the user's time slots into
        1-hour block objects for json storage.
        """
        # Generate days with various scopes.
        # day1 8am - 10am, length should be 2, {8-9},{9-10}.
        test_day1 = create_day_array(8, 10)
        self.assertEqual(len(test_day1), 2)
        
        # Make sure days with -1 return empty array.
        test_day2 = create_day_array(-1, 15)
        test_day3 = create_day_array(10, -1)
        test_day4 = create_day_array(-1, -1)
        self.assertEqual(test_day2, [])
        self.assertEqual(test_day3, [])
        self.assertEqual(test_day4, [])

    def test_day_array_input(self):
        """Testing the input of day_array."""
        self.assertRaises(TypeError, create_day_array, True)
        

