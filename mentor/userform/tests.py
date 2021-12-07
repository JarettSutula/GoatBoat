import unittest
from mentor.utils import create_day_array, collection_link, start_db, restructure_day_array

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

    # def test_start_db(self):
    #     """Testing the connection to the database."""
    #     result = start_db()
    #     self.assertEqual(result.list_collection_names()[0], 'users')

    # def test_collection_link(self):
    #     """Testing the connection to a specific collection in db."""
    #     my_db = start_db()
    #     my_collection = collection_link(my_db, 'users')
    #     self.assertGreater(my_collection.estimated_document_count(), 0)

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

if __name__ == '__main__':
    unittest.main()


