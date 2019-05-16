from django.test import TestCase

from recipe_management_project.calc import add
# Create your tests here.

class CalcTests(TestCase):

    def test_add_numbers(self):
        """Test that two numbers are added together"""
        self.assertEqual(add(3, 8), 11)