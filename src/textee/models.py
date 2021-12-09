from pygments.lexers import get_all_lexers

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .utils import make_random_string

User = get_user_model()
LEXERS = [item for item in get_all_lexers() if item[1]]
SYNTAX_CHOICES = [("", "Нет")] + sorted([(item[1][0], item[0]) for item in LEXERS])


class InactiveSnippetManager(models.Manager):
    def get_queryset(self):
        """Возвращает сниппеты, срок действия которых истёк."""
        return super().get_queryset().filter(expiration__lte=timezone.now())


class ActiveSnippetManager(models.Manager):
    def get_queryset(self):
        """Возвращает сниппеты, срок действия которых не истёк."""
        return super().get_queryset().exclude(expiration__lte=timezone.now())


class Snippet(models.Model):
    """Сниппет - фрагмент исходного текста или кода программы."""

    DEFAULT_TITLE = "Без названия"
    URL_LENGTH = 8
    CODE_MAX_LENGTH = 65_536  # не более 256 KiB (utf-8)

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="snippets"
    )
    title = models.CharField(
        verbose_name="Заголовок",
        max_length=100,
        blank=True,
        default=DEFAULT_TITLE,
    )
    code = models.CharField(verbose_name="Текст", max_length=CODE_MAX_LENGTH)
    syntax = models.CharField(
        verbose_name="Подсветка синтаксиса",
        choices=SYNTAX_CHOICES,
        max_length=100,
        blank=True,
    )
    created = models.DateTimeField(verbose_name="Создан", auto_now_add=True)
    expiration = models.DateTimeField(
        verbose_name="Срок действия", null=True, blank=True
    )
    url = models.CharField(max_length=URL_LENGTH, unique=True, editable=False)

    # managers
    objects = models.Manager()
    inactive = InactiveSnippetManager()
    active = ActiveSnippetManager()

    class Meta:
        verbose_name = "Сниппет"
        verbose_name_plural = "Сниппеты"

    def __str__(self) -> str:
        return f"Сниппет: {self.title}"

    def save(self, *args, **kwargs) -> None:
        self.title = self.title or self.DEFAULT_TITLE
        self.url = self.url or self._generate_unique_url()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("snippet_detail", kwargs={"url": self.url})

    def _generate_unique_url(self) -> str:
        url = make_random_string(self.URL_LENGTH)
        if Snippet.objects.filter(url=url).exists():
            return self._generate_unique_url()
        return url
