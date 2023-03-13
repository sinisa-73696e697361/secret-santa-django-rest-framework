"""
Tests for user API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create-user")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:current-user")


def create_user(**user_parameters):
    """
    Creates and returns a user
    :param user_parameters:
    :return: user
    """
    return get_user_model().objects.create_user(**user_parameters)


class UserApiTests(TestCase):
    """
    User API tests
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_user_successful(self):
        """
        Test creating a new user
        """
        user_parameters = {
            "email": "test@example.com",
            "password": "test_password_123",  # noqa
            "first_name": "Test",
            "last_name": "User",
        }

        result = self.client.post(CREATE_USER_URL, user_parameters)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=user_parameters["email"])
        self.assertTrue(user.check_password(user_parameters["password"]))
        self.assertNotIn("password", result.data)

    def test_create_user_email_already_exists(self):
        """
        Test creating a new user if email already exists in DB
        """
        user_parameters = {
            "email": "test@example.com",
            "password": "test_password_123",  # noqa
            "first_name": "Test",
            "last_name": "User",
        }
        create_user(**user_parameters)
        result = self.client.post(CREATE_USER_URL, user_parameters)

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token(self):
        """
        Test create_token with correct credentials
        """
        user_parameters = {
            "email": "test@example.com",
            "password": "test_password_123",  # noqa
            "first_name": "Test",
            "last_name": "User",
        }
        create_user(**user_parameters)

        payload = {
            "email": user_parameters["email"],
            "password": user_parameters["password"],
        }
        result = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", result.data)
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """
        Test create_token with incorrect credentials
        """
        user_parameters = {
            "email": "test@example.com",
            "password": "correct_password",  # noqa
            "first_name": "Test",
            "last_name": "User",
        }
        create_user(**user_parameters)

        payload = {
            "email": "test@example.com",
            "password": "incorrect_password",  # noqa
        }
        result = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", result.data)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """
        Test that token is not created if user doesn't exist
        """
        payload = {"email": "test@example.com", "password": "test_password_123"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        Test that authentication is required for users
        """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """
    Test API requests that require authentication
    """

    def setUp(self):
        password = "test_password_123"  # noqa
        self.user = create_user(
            email="test@example.com",
            password=password,
            first_name="Test",
            last_name="User",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """
        Test retrieving profile for logged in used
        """
        result = self.client.get(ME_URL)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(
            result.data,
            {
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email,
            },
        )

    def test_update_user_profile(self):
        """
        Test updating the user profile for authenticated user
        """
        payload = {"first_name": "TestTest", "password": "new_password"}

        result = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload["first_name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(result.status_code, status.HTTP_200_OK)
