import unittest
from utils import create_day_array, collection_link, start_db

class TestFormCreation(unittest.TestCase):
    """Tests functions within create_user_form."""

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
        10pm, indicated by integer values 8-22."""
        with self.assertRaises(ValueError):
            create_day_array(-5, 10)
        with self.assertRaises(ValueError):
            create_day_array(10, 23)

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

if __name__ == '__main__':
    unittest.main()