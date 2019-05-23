from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successfull"""
        email = 'test@arbisoft.com'
        name = 'test_arbisoft'
        password = 'testpassword'
        user = get_user_model().objects.create_user(
            email=email,
            name=name,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@ArbiSoft.com'
        user = get_user_model().objects.create_user(
            email=email,
            name='test_name',
            password="test_password"
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_valid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                name="test_name",
                password="test_password"
                )

    def test_create_new_superuser(self):
        """Test creating a new supperuser"""
        user = get_user_model().objects.create_superuser(
            email="test@arbisoft.com",
            name="test_name",
            password="test_apssword"
            )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
