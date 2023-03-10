"""
Tests for Django admin
"""
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    """
    Tests for Django admin
    """

    def setUp(self):
        """
        Create user and client
        """
        admin_email = "admin@example.com"
        admin_password = "admin_password_123"  # noqa
        user_email = "test_user@example.com"
        user_password = "admin_password_123"  # noqa
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email=admin_email, password=admin_password
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email=user_email,
            password=user_password,
            first_name="Test",
            last_name="User",
        )

    def test_users_list(self):
        """
        Testing that users are listed on admin page
        """
        url = reverse("admin:core_user_changelist")
        result = self.client.get(url)

        self.assertContains(result, self.user)
        self.assertContains(result, self.admin_user)

    def test_edit_user_page(self):
        """
        Testing edit functionality on admin page
        """
        url = reverse("admin:core_user_change", args=[self.user.id])
        result = self.client.get(url)

        self.assertEqual(result.status_code, 200)

    def test_create_user_page(self):
        """
        Testing create functionality on admin page
        """
        url = reverse("admin:core_user_add")
        result = self.client.get(url)

        self.assertEqual(result.status_code, 200)
