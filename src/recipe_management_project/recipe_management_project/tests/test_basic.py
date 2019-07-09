"""
Sample module to create the sample test cases for the calc module
"""
from django.test import TestCase

from ..calc import add, substract


class CalcTests(TestCase):
    """Used to craete the sample unit tests for the calc module"""

    def test_add_numbers(self):
        """Test that two numbers are added together"""
        self.assertEqual(add(3, 8), 11)

    def test_substract_numbers(self):
        """Test that values are substracted and returned"""
        self.assertEqual(substract(5, 11), 6)
