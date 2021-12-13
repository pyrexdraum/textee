from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        ordering = ("-date_joined",)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"username": self.username})
