"""
Tests for models
"""
from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTests(TestCase):
    """
    Tests for User model
    """

    def test_create_user_with_email_successful(self):
        """
        Test creating a new user
        """
        email = "test@example.com"
        password = "test_password_123"  # noqa
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalize_email(self):
        """
        Test functionality to normalize email address
        """
        sample_emails = [
            ["test1@EXAMPLE.COM", "test1@example.com"],
            ["Test2@EXAMPLE.com", "Test2@example.com"],
            ["tEsT3@ExAmPlE.cOm", "tEsT3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        password = "test_password_123"  # noqa
        for email in sample_emails:
            user = get_user_model().objects.create_user(
                email=email[0], password=password
            )
            self.assertEqual(user.email, email[1])

    def test_new_user_without_email_raises_error(self):
        """
        Test for creating new user without email
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test_password_123")

    def test_create_superuser(self):
        """
        Test for creating a superuser
        """
        email = "test@example.com"
        password = "test_password_123"  # noqa
        user = get_user_model().objects.create_superuser(email=email, password=password)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
