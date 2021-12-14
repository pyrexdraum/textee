from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..forms import SnippetForm
from ..models import Snippet
from ..service import highlight_code

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


class SnippetDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.snippet = Snippet.objects.create(code="1")
        cls.snippet_with_syntax = Snippet.objects.create(code="2", syntax="python")

    def test_uses_detail_template(self):
        response = self.client.get(self.snippet.get_absolute_url())
        self.assertTemplateUsed(response, "textee/detail.html")

    def test_highlighted_code_in_context_if_syntax_is_not_empty(self):
        snippet = self.snippet_with_syntax
        highlighted_code = highlight_code(code=snippet.code, syntax=snippet.syntax)

        response = self.client.get(snippet.get_absolute_url())
        self.assertEqual(response.context["highlighted_code"], highlighted_code)

    def test_highlighted_code_not_in_context_if_syntax_is_empty(self):
        snippet = Snippet.objects.create(code="1")
        response = self.client.get(snippet.get_absolute_url())
        with self.assertRaises(KeyError):
            response.context["highlighted_code"]

    def test_snippet_in_context(self):
        response = self.client.get(self.snippet.get_absolute_url())
        self.assertEqual(response.context["snippet"], self.snippet)


class SnippetDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.snippet_owner = User.objects.create(username="testuser")
        snippet = Snippet.objects.create(owner=cls.snippet_owner, code="321")
        cls.snippet_delete_url = reverse("snippet_delete", kwargs={"url": snippet.url})

    def test_not_authenticated_user_cannot_delete_snippet(self):
        response = self.client.post(self.snippet_delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Snippet.objects.count(), 1)

    def test_owner_of_snippet_can_delete_it(self):
        self.client.force_login(self.snippet_owner)
        response = self.client.post(self.snippet_delete_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Snippet.objects.count(), 0)

    def test_only_owner_can_delete_his_snippet(self):
        not_owner = User.objects.create(username="not_owner")
        self.client.force_login(not_owner)

        response = self.client.post(self.snippet_delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Snippet.objects.count(), 1)

    def test_redirects_to_profile_after_delete(self):
        self.client.force_login(self.snippet_owner)
        response = self.client.post(self.snippet_delete_url)
        self.assertRedirects(response, self.snippet_owner.get_absolute_url())
