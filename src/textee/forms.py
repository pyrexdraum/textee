from datetime import timedelta
from typing import Optional

from django import forms
from django.utils import timezone

from .models import Snippet


class SnippetForm(forms.ModelForm):
    NO_TIME = "N"
    TEN_MINUTES = "10"
    ONE_HOUR = "1H"
    ONE_DAY = "1D"
    ONE_WEEK = "1W"
    ONE_MONTH = "1M"
    HALF_YEAR = "6M"
    ONE_YEAR = "1Y"
    EXPIRATION_CHOICES = (
        (NO_TIME, "Не удалять"),
        (TEN_MINUTES, "10 минут"),
        (ONE_HOUR, "1 час"),
        (ONE_DAY, "1 день"),
        (ONE_WEEK, "1 неделя"),
        (ONE_MONTH, "1 месяц"),
        (HALF_YEAR, "Пол года"),
        (ONE_YEAR, "1 год"),
    )
    EXPIRATION_IN_TIMEDELTA = {
        TEN_MINUTES: timedelta(minutes=10),
        ONE_HOUR: timedelta(hours=1),
        ONE_DAY: timedelta(days=1),
        ONE_WEEK: timedelta(weeks=1),
        ONE_MONTH: timedelta(days=30),
        HALF_YEAR: timedelta(days=366 // 2),
        ONE_YEAR: timedelta(days=366),
    }

    expiration = forms.ChoiceField(
        label="Срок действия",
        choices=EXPIRATION_CHOICES,
        required=False,
    )

    class Meta:
        model = Snippet
        fields = ("title", "code", "syntax", "expiration")
        widgets = {"code": forms.Textarea()}

    def clean_expiration(self) -> Optional[timezone.datetime]:
        time_code = self.cleaned_data["expiration"]
        if time_code not in self.EXPIRATION_IN_TIMEDELTA:
            return None

        return timezone.now() + self.EXPIRATION_IN_TIMEDELTA[time_code]
