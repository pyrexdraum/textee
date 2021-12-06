from datetime import timedelta

from django import forms
from django.utils import timezone
from django.db import models

from .models import Snippet


class SnippetForm(forms.ModelForm):

    class Timer(models.TextChoices):
        FOREVER = ("N", "Не удалять")
        TEN_MINUTES = ("10", "10 минут")
        ONE_HOUR = ("1H", "1 час")
        ONE_DAY = ("1D", "1 день")
        ONE_WEEK = ("1W", "1 неделя")
        ONE_MONTH = ("1M", "1 месяц")
        SIX_MONTHS = ("6M", "6 месяцев")
        ONE_YEAR = ("1Y", "1 год")

        @classmethod
        def get_timer(cls, time_code):
            time_code_in_minutes = {
                cls.TEN_MINUTES: 10,
                cls.ONE_HOUR:    60,
                cls.ONE_DAY:     60 * 24,
                cls.ONE_WEEK:    60 * 24 * 7,
                cls.ONE_MONTH:   60 * 24 * 7 * 4,
                cls.SIX_MONTHS:  60 * 24 * 7 * 4 * 6,
                cls.ONE_YEAR:    60 * 24 * 7 * 4 * 12,
            }
            if time_code == cls.FOREVER:
                return None
            elif time_code not in time_code_in_minutes:
                raise ValueError()

            return timezone.now() + timedelta(minutes=time_code_in_minutes[time_code])

    expiration = forms.TypedChoiceField(
        label="Срок действия",
        choices=Timer.choices,
        coerce=Timer.get_timer,
        empty_value=None,
        required=False,
    )

    class Meta:
        model = Snippet
        fields = ("title", "code", "syntax", "expiration")
        widgets = {
            "code": forms.Textarea()
        }
