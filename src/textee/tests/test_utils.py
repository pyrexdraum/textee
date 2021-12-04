from unittest import TestCase
from string import ascii_letters, digits

from ..utils import make_random_string


class MakeRandomStringTest(TestCase):

    def test_positive_integer_length(self):
        """
        Целое положительное число для length
        возвращает строку длиной length.
        """
        for length in range(10):
            string = make_random_string(length)
            self.assertEqual(len(string), length)

    def test_negative_integer_length(self):
        """
        Целое отрицательное число для length возвращает пустую строку.
        """
        for length in range(-10, 0):
            string = make_random_string(length)
            self.assertEqual(string, "")

    def test_chars_argument(self):
        """
        Возвращаемая строка состоит только из символов chars.
        """
        chars = "ABC"
        string = make_random_string(length=10, chars=chars)
        for char in string:
            self.assertIn(char, chars)

    def test_default_chars(self):
        """
        По умолчанию chars состоит из цифр и букв ASCII.
        """
        default_chars = ascii_letters + digits
        string = make_random_string(100)
        for char in string:
            self.assertIn(char, default_chars)
