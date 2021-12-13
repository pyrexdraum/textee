from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from textee.models import Snippet

User = get_user_model()


class ProfileDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="testuser")

    def test_uses_template(self):
        response = self.client.get(self.user.get_absolute_url())
        self.assertTemplateUsed(response, "accounts/profile.html")

    def test_display_user_snippets(self):
        response = self.client.get(self.user.get_absolute_url())
        self.assertNotContains(response, "fizzbuzz")

        Snippet.objects.create(owner=self.user, title="fizzbuzz", code="1")
        response = self.client.get(self.user.get_absolute_url())
        self.assertContains(response, "fizzbuzz")


class UserModelTest(TestCase):
    def test_get_absolute_url(self):
        user = User.objects.create(username="fizzbuzz")
        expected_url = reverse("profile", kwargs={"username": user.username})
        self.assertEqual(user.get_absolute_url(), expected_url)
