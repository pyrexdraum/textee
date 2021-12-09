from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from ..models import Snippet


class SnippetModelTest(TestCase):
    def create_3_snippets_with_different_expiration(self):
        """
        Создаёт 3 сниппета с разными сроками действий:
        истёкшим, не истёкшим и без срока действия.
        """
        now = timezone.now()
        past_time = now - timedelta(minutes=1)
        future_time = now + timedelta(minutes=1)

        Snippet.objects.create(title="Expired", expiration=past_time)
        Snippet.objects.create(title="Not Expired", expiration=future_time)
        Snippet.objects.create(title="No Expiration")  # без срока

    def test_save_method_sets_default_title_if_title_is_empty(self):
        snippet = Snippet.objects.create(title="", code="1")
        self.assertEqual(snippet.title, Snippet.DEFAULT_TITLE)

    def test_string_representation(self):
        snippet = Snippet(title="FooBar")
        self.assertEqual(str(snippet), "Сниппет: FooBar")

    def test_get_absolute_url(self):
        snippet = Snippet.objects.create()
        self.assertEqual(snippet.get_absolute_url(), f"/{snippet.url}/")

    def test_generate_unique_url_returns_url_with_default_length(self):
        url = Snippet()._generate_unique_url()
        self.assertEqual(len(url), Snippet.URL_LENGTH)

    def test_save_method_sets_url(self):
        snippet = Snippet()
        self.assertFalse(snippet.url)

        snippet.save()
        self.assertTrue(snippet.url)

    def test_inactive_snippets(self):
        """
        Менеджер inactive возвращает только сниппеты с истёкшим сроком.
        """
        self.create_3_snippets_with_different_expiration()
        self.assertEqual(Snippet.objects.count(), 3)

        expired_snippet = Snippet.objects.filter(expiration__lt=timezone.now())
        self.assertEqual(len(expired_snippet), 1)
        self.assertQuerysetEqual(Snippet.inactive.order_by("created"), expired_snippet)

    def test_active_snippets(self):
        """
        Менеджер active возвращает только те сниппеты,
        срок действия которых не истёк.
        """
        self.create_3_snippets_with_different_expiration()
        self.assertEqual(Snippet.objects.count(), 3)

        not_expired_snippets = Snippet.objects.exclude(
            expiration__lt=timezone.now()
        ).order_by("created")
        self.assertEqual(len(not_expired_snippets), 2)
        self.assertQuerysetEqual(
            Snippet.active.order_by("created"), not_expired_snippets
        )

    def test_url_doesnt_change_after_update(self):
        snippet = Snippet.objects.create(code="123")
        url_before_update = snippet.url

        snippet.code = "321"
        snippet.save()

        snippet.refresh_from_db()
        url_after_update = snippet.url
        self.assertEqual(url_after_update, url_before_update)
