from datetime import timedelta
from typing import Optional

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit

from django import forms
from django.utils import timezone

from .models import Snippet


class SnippetForm(forms.ModelForm):
    CODE_PLACEHOLDER = """
        Textee - это веб-сайт, на котором вы можете хранить любой текст
        онлайн для удобства обмена. Веб-сайт в основном используется 
        программистами для хранения фрагментов исходного кода или 
        информации о конфигурации, но любой желающий может вставить 
        любой тип текста, выбрать срок действия и синтаксис.
        
        Начните печатать или вставьте текст...
        """
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "index"
        self.helper.form_class = "row g-3"
        self.helper.layout = Layout(
            Div(Field("code", placeholder=self.CODE_PLACEHOLDER), css_class="col-12"),
            Div("title", css_class="col-5"),
            Div("syntax", css_class="col-5"),
            Div("expiration", css_class="col-2"),
            Div(Submit("create", "Создать", css_class="btn btn-success")),
        )

    def clean_expiration(self) -> Optional[timezone.datetime]:
        time_code = self.cleaned_data["expiration"]
        if time_code not in self.EXPIRATION_IN_TIMEDELTA:
            return None

        return timezone.now() + self.EXPIRATION_IN_TIMEDELTA[time_code]
