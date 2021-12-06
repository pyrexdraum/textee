from django.test import TestCase
from django.contrib.auth import get_user_model

from ..forms import SnippetForm
from ..models import Snippet

User = get_user_model()


class SnippetCreateViewTest(TestCase):

    def test_uses_index_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "textee/index.html")

    def test_uses_form(self):
        response = self.client.get("/")
        self.assertIsInstance(response.context["form"], SnippetForm)

    def test_can_save_post_request(self):
        self.client.post("/", data={"code": "Just a code.", "syntax": "none"})
        self.assertEqual(Snippet.objects.count(), 1)
        snippet = Snippet.objects.first()
        self.assertEqual(snippet.code, "Just a code.")

    def test_snippet_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(username="test")
        self.client.force_login(user)
        payload = {"code": "123", "syntax": "none"}
        self.client.post("/", data=payload)
        snippet = Snippet.objects.first()
        self.assertEqual(snippet.owner, user)

    def test_redirects_after_save(self):
        response = self.client.post("/", data={"code": "1", "syntax": "none"})
        created_snippet = Snippet.objects.first()
        self.assertRedirects(response, f"/{created_snippet.url}/")
