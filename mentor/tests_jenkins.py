import unittest

# if the user is jenkins, import utils from mentor to not have 'module not found' error.
from mentor.utils import create_day_array, find_matching_schedule, get_time_string, restructure_day_array

class TestMethods(unittest.TestCase):
    """Tests functions from util helper functions."""

    def test_day_array_length(self):
        """Testing the create_day_array function. This is normally called
        in the profile creation form to turn the user's time slots into
        1-hour block objects for json storage.
        """
        # Generate days with various scopes.
        # day1 8am - 12pm, length should be 4, {8-9},{9-10},{10-11},{11-12}
        test_day1 = create_day_array(8, 12)
        self.assertEqual(len(test_day1), 4)

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
        10pm, indicated by integer values 8-22. Test if first value is invalid.
        """
        with self.assertRaises(ValueError):
            create_day_array(-5, 10)
        
    def test_day_array_ranges_2(self):
        """test if only last value is invalid."""
        with self.assertRaises(ValueError):
            create_day_array(10, 23)

    def test_day_array_ranges_3(self):
        """test if both values are invalid."""
        with self.assertRaises(ValueError):
            create_day_array(4, 23)

    def test_day_array_input(self):
        """Testing the input of day_array."""
        with self.assertRaises(TypeError):
            create_day_array('string', 1)

    def test_restructure_day_array_valid(self):
        """Testing if an empty day returns invalid numbers."""
        test_day = {}
        test_day_restructured = restructure_day_array(test_day)
        self.assertEqual(test_day_restructured, (-1, -1))

    def test_restructure_day_array_valid_2(self):
        """Testing if one-hour block day works correctly."""
        test_day = [{'starttime': 8, 'endtime': 9}]
        # should return (8, 9).
        test_day_restructured = restructure_day_array(test_day)
        self.assertEqual(test_day_restructured, (8, 9))

    def test_restructure_day_array_valid_3(self):
        """Testing if multiple-hour block day works correctly."""
        test_day = [{'starttime': 8, 'endtime': 9}, {'starttime': 9, 'endtime': 10}]
        # should return (8, 10).
        test_day_restructured = restructure_day_array(test_day)
        self.assertEqual(test_day_restructured, (8, 10))

    def test_find_matching_schedule_none(self):
        """Test specifically if there is no matching blocks."""
        test_user_1 = {'monday': [{'starttime':8, 'endtime': 9}],
                       'tuesday': [],
                       'wednesday': [],
                       'thursday': [],
                       'friday': [],
                       'saturday': [],
                       'sunday': []
                       }

        test_user_2 = {'monday': [],
                       'tuesday': [],
                       'wednesday': [],
                       'thursday': [],
                       'friday': [],
                       'saturday': [],
                       'sunday': [{'starttime':10, 'endtime': 11}]
                       }

        match = find_matching_schedule(test_user_1, test_user_2)
        self.assertIsNone(match)

    def test_find_matching_schedule_true(self):
        """Test that it matches at the same time."""
        test_user_1 = {'monday': [{'starttime':10, 'endtime': 11}],
                       'tuesday': [],
                       'wednesday': [],
                       'thursday': [],
                       'friday': [],
                       'saturday': [],
                       'sunday': []
                       }

        test_user_2 = {'monday': [{'starttime':10, 'endtime': 11}],
                       'tuesday': [],
                       'wednesday': [],
                       'thursday': [],
                       'friday': [],
                       'saturday': [],
                       'sunday': []
                       }

        match = find_matching_schedule(test_user_1, test_user_2)
        self.assertEqual(match['day'], 'Monday')
        self.assertEqual(match['starttime'], 10)
        self.assertEqual(match['endtime'], 11)

    def test_find_matching_schedule_first(self):
        """Test that it matches specifically the first block."""
        test_user_1 = {'monday': [{'starttime':10, 'endtime': 11}],
                       'tuesday': [],
                       'wednesday': [{'starttime':10, 'endtime': 11}],
                       'thursday': [],
                       'friday': [],
                       'saturday': [],
                       'sunday': []
                       }

        test_user_2 = {'monday': [{'starttime':10, 'endtime': 11}],
                       'tuesday': [],
                       'wednesday': [{'starttime':10, 'endtime': 11}],
                       'thursday': [],
                       'friday': [],
                       'saturday': [],
                       'sunday': []
                       }

        match = find_matching_schedule(test_user_1, test_user_2)
        self.assertEqual(match['day'], 'Monday')

    def test_get_time_string_am(self):
        """Test to make sure an early morning block is correct to display."""
        # 8 --> 8:00am
        test_hour = 8
        test_hour_stringified = get_time_string(test_hour)
        self.assertEqual(test_hour_stringified, "8:00am")

    def test_get_time_string_noon(self):
        """Test to make sure noon-block display 12:00pm not am."""
        # 12 --> 12:00pm 
        test_hour = 12
        test_hour_stringified = get_time_string(test_hour)
        self.assertEqual(test_hour_stringified, "12:00pm")

    def test_get_time_string_pm(self):
        """Test to make sure evening hours generate correctly."""
        # 16 --> 4:00pm 
        test_hour = 16
        test_hour_stringified = get_time_string(test_hour)
        self.assertEqual(test_hour_stringified, "4:00pm")

    def test_get_time_string_valid(self):
        """Test to make sure invalid times get None back."""
        # 23 --> 11:00pm , invalid, return None
        test_hour = 23
        test_hour_stringified = get_time_string(test_hour)
        self.assertIsNone(test_hour_stringified)

if __name__ == '__main__':
    unittest.main()


