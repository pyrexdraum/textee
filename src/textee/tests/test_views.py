from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..forms import SnippetForm
from ..models import Snippet

User = get_user_model()


class SnippetCreateViewTest(TestCase):
    def test_uses_index_template(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "textee/index.html")

    def test_uses_form(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.context["form"], SnippetForm)

    def test_can_save_post_request(self):
        self.client.post("/", data={"code": "Just a code."})
        self.assertEqual(Snippet.objects.count(), 1)

        snippet = Snippet.objects.first()
        self.assertEqual(snippet.code, "Just a code.")

    def test_snippet_owner_is_set_for_authenticated_user(self):
        user = User.objects.create(username="test")
        self.client.force_login(user)
        self.client.post("/", {"code": "authenticated"})

        snippet = Snippet.objects.first()
        self.assertEqual(snippet.owner, user)

    def test_snippet_owner_is_none_if_user_not_authenticated(self):
        self.client.post("/", {"code": "not authenticated"})
        snippet = Snippet.objects.first()
        self.assertIsNone(snippet.owner)

    def test_redirects_after_save(self):
        response = self.client.post("/", data={"code": "redirected"})
        snippet = Snippet.objects.first()
        self.assertRedirects(response, f"/{snippet.url}/")

    def test_for_invalid_input_doesnt_save(self):
        response = self.client.post("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Snippet.objects.count(), 0)
