from datetime import timedelta

from django.test import SimpleTestCase
from django.utils import timezone

from ..forms import SnippetForm


class SnippetFormTest(SimpleTestCase):

    def test_form_with_valid_data(self):
        """
        Форма требует заполнить только поле code и syntax.
        """
        form = SnippetForm({"code": "Just a code.", "syntax": "none"})
        self.assertIs(form.is_valid(), True)

    def test_expiration_field_with_invalid_choice(self):
        form = SnippetForm({"expiration": "FooBar"})
        self.assertTrue(form["expiration"].errors)

    def test_expiration_field_with_valid_choice(self):
        for choice in SnippetForm.Timer.choices:
            form = SnippetForm({"expiration": choice[0]})
            self.assertFalse(form["expiration"].errors)

    def test_get_timer(self):
        """
        Timer.get_timer() возвращает соответствующий объект datetime.
        """
        expected_time = timedelta(minutes=10)
        inaccuracy = timedelta(seconds=2)

        time_code = SnippetForm.Timer.TEN_MINUTES
        output_time = SnippetForm.Timer.get_timer(time_code) - timezone.now()

        result = (expected_time - inaccuracy) <= output_time <= expected_time
        self.assertTrue(result)
