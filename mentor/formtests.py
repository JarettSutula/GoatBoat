import unittest

from utils import create_day_array

class TestFormCreation(unittest.TestCase):
    """Tests functions within create_user_form."""

    def test_day_array_length(self):
        """Testing the create_day_array function. This is normally called
        in the profile creation form to turn the user's time slots into
        1-hour block objects for json storage.
        """
        # Generate days with various scopes.
        # day1 8am - 10am, length should be 2, {8-9},{9-10}.
        test_day1 = create_day_array(8, 10)
        self.assertEqual(len(test_day1), 2)

    def test_day_array_empty(self):
        """create_day_array should return empty arrays if given incorrect
        values.
        """
        # Make sure days with -1 return empty array.
        test_day1 = create_day_array(-1, 15)
        test_day2 = create_day_array(10, -1)
        test_day3 = create_day_array(-1, -1)
        self.assertEqual(test_day1, [])
        self.assertEqual(test_day2, [])
        self.assertEqual(test_day3, [])

    def test_day_array_ranges(self):
        """create_day_array needs to only return time frames between 8am and
        10pm, indicated by integer values 8-22."""
        with self.assertRaises(ValueError):
            test_day1 = create_day_array(-5, 10)
        with self.assertRaises(ValueError):
            test_day2 = create_day_array(10, 23)
            
        test_day3 = create_day_array(8, 22)

    def test_day_array_input(self):
        """Testing the input of day_array."""
        with self.assertRaises(TypeError):
            test_day1 = create_day_array('string', 1)
        

if __name__ == '__main__':
    unittest.main()