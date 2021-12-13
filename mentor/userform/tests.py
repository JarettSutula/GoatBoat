from django.test import TestCase
import os
import unittest


# Create your tests here.

class TestMethods(unittest.TestCase):

    def test_quicktest(self):
        self.assertEqual('wow', 'wow')


if __name__ == '__main__':
    unittest.main()


