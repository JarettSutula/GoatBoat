import unittest
from .utils import create_day_array, collection_link, find_matching_schedule, get_time_string, start_db, restructure_day_array, get_profile_snapshot, dynamic_class_dropdown

# Create your tests here.

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

    def test_start_db(self):
        """Testing the connection to the database."""
        result = start_db()
        self.assertEqual(result.list_collection_names()[0], 'users')

    def test_collection_link(self):
        """Testing the connection to a specific collection in db."""
        my_db = start_db()
        my_collection = collection_link(my_db, 'users')
        self.assertGreater(my_collection.estimated_document_count(), 0)

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

    def test_get_profile_snapshot_invalid(self):
        """Test that profile snapshots return a failed profile."""
        # make sure we use a name that doesn't exist.
        # should return profile = {'failed':True}
        test_profile = get_profile_snapshot('totallyrandomguy685', True)
        self.assertEqual(test_profile['failed'], True) 

    def test_get_profile_snapshot_valid_not_full(self):
        """Test that a valid profile returns only the shortened version
        when the 'full_profile' parameter is false.
        """
        # test the 'donotdelete' user with small snapshot.
        test_profile = get_profile_snapshot('donotdelete', False)

        # see if email is returned. It shouldn't be.
        does_email_exist = True
        if 'firstname' in test_profile and 'email' not in test_profile:
            # if we have the username but not the email, we got the small snapshot.
            does_email_exist = False

        self.assertFalse(does_email_exist)

    def test_get_profile_snapshot_valid_full(self):
        """Test that a valid profile returns only the shortened version
        when the 'full_profile' parameter is true.
        """
        # test the 'donotdelete' user with full snapshot.
        test_profile = get_profile_snapshot('donotdelete', True)

        # see if email is returned. It should.
        does_email_exist = False
        if 'firstname' in test_profile and 'email' in test_profile:
            # if we have the username and the email, we got the full snapshot.
            does_email_exist = True

        self.assertTrue(does_email_exist)

    def test_dynamic_class_dropdown_invalid_mentor(self):
        """Test dynamic class dropdown raises error if invalid as a mentor."""
        with self.assertRaises(ValueError):
            dynamic_class_dropdown('totallyrandomguy685', 'mentor')

    def test_dynamic_class_dropdown_invalid_mentee(self):
        """Test dynamic class dropdown raises error if invalid as a mentee."""
        with self.assertRaises(ValueError):
            dynamic_class_dropdown('totallyrandomguy685', 'mentee')

    def test_dynamic_class_dropdown_valid_mentor(self):
        """Test dynamic class dropdown returning correct values as a mentor."""
        # user donotdelete has 1 class as a mentor - MATH393
        test_class_choices = dynamic_class_dropdown('donotdelete', 'mentor')

        # assert length 1 and that the class is Math393.
        self.assertEqual(len(test_class_choices), 1)
        self.assertEqual(test_class_choices[0][0], 'MATH393')
        self.assertEqual(test_class_choices[0][1], 'MATH 393')
    
    def test_dynamic_class_dropdown_valid_mentee(self):
        """Test dynamic class dropdown returning correct values as a mentee."""
        # user donotdelete has 1 class as a mentee - MATH394
        test_class_choices = dynamic_class_dropdown('donotdelete', 'mentee')

        # assert length 1 and that the class is Math394.
        self.assertEqual(len(test_class_choices), 1)
        self.assertEqual(test_class_choices[0][0], 'MATH394')
        self.assertEqual(test_class_choices[0][1], 'MATH 394')


if __name__ == '__main__':
    unittest.main()


