from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from ..models import Snippet


class SnippetModelTest(TestCase):
    def test_empty_title_sets_default_title(self):
        snippet = Snippet.objects.create(title="", code="1")
        self.assertEquals(snippet.title, Snippet.DEFAULT_TITLE)

    def test_string_representation(self):
        snippet = Snippet(title="FooBar")
        self.assertEquals(str(snippet), "Сниппет: FooBar")

    def test_get_absolute_url(self):
        snippet = Snippet.objects.create()
        self.assertEquals(snippet.get_absolute_url(), f"/{snippet.url}/")

    def test_generate_unique_url_returns_url_with_default_length(self):
        url = Snippet()._generate_unique_url()
        self.assertEquals(len(url), Snippet.URL_LENGTH)

    def test_save_method_sets_url(self):
        snippet = Snippet()
        self.assertFalse(snippet.url)

        snippet.save()
        self.assertTrue(snippet.url)

    def test_code_content(self):
        expected_code = "Just a code."
        snippet = Snippet.objects.create(code=expected_code)
        self.assertEquals(snippet.code, expected_code)

    def test_inactive_snippets(self):
        """
        Менеджер inactive возвращает только сниппеты с истёкшим сроком.
        """
        inactive_snippets = [
            Snippet.objects.create(expiration=timezone.now() - timedelta(seconds=1)),
            Snippet.objects.create(expiration=timezone.now() - timedelta(days=1)),
        ]
        Snippet.objects.create()
        Snippet.objects.create(expiration=timezone.now() + timedelta(days=1))

        self.assertQuerysetEqual(
            Snippet.inactive.order_by("created"), inactive_snippets
        )

    def test_active_snippets(self):
        """
        Менеджер active возвращает только сниппеты,
        срок действия которых не истёк.
        """
        active_snippets = [
            Snippet.objects.create(),
            Snippet.objects.create(expiration=timezone.now() + timedelta(days=1)),
        ]
        Snippet.objects.create(expiration=timezone.now() - timedelta(seconds=1)),
        Snippet.objects.create(expiration=timezone.now() - timedelta(days=1))

        self.assertQuerysetEqual(Snippet.active.order_by("created"), active_snippets)

    def test_objects(self):
        """
        Менеджер objects возвращает все сниппеты.
        """
        snippets = [
            Snippet.objects.create(),
            Snippet.objects.create(expiration=timezone.now() + timedelta(days=1)),
            Snippet.objects.create(expiration=timezone.now() - timedelta(seconds=1)),
            Snippet.objects.create(expiration=timezone.now() - timedelta(days=1)),
        ]

        self.assertQuerysetEqual(Snippet.objects.order_by("created"), snippets)

    def test_url_doesnt_change_after_update(self):
        snippet = Snippet.objects.create(code="123")
        url_before_update = snippet.url
        snippet.code = "321"
        snippet.save()
        snippet.refresh_from_db()
        url_after_update = snippet.url
        self.assertEquals(url_after_update, url_before_update)
