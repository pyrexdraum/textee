from django.test import TestCase

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
