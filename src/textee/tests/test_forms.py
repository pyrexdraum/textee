from datetime import datetime

from django.test import SimpleTestCase

from ..forms import SnippetForm


class SnippetFormTest(SimpleTestCase):
    def test_form_with_valid_data(self):
        """
        Форма требует заполнить только поле code.
        """
        form = SnippetForm({"code": "Just a code."})
        self.assertIs(form.is_valid(), True)

    def test_expiration_field_with_invalid_choice(self):
        form = SnippetForm({"expiration": "FooBar"})
        self.assertTrue(form["expiration"].errors)

    def test_expiration_field_with_valid_choice(self):
        for choice in SnippetForm.EXPIRATION_CHOICES:
            form = SnippetForm({"expiration": choice[0]})
            self.assertFalse(form["expiration"].errors)

    def test_clean_expiration_returns_datetime_for_valid_value(self):
        """
        clean_expiration() возвращает объект datetime для значений
        из SnippetForm.EXPIRATION_IN_TIMEDELTA.
        """
        for time_code in SnippetForm.EXPIRATION_IN_TIMEDELTA:
            form = SnippetForm({"expiration": time_code})
            form.is_valid()
            expiration = form.cleaned_data.get("expiration", None)
            self.assertIsInstance(expiration, datetime)
