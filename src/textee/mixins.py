from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from .models import Snippet


class OwnerSnippetRequiredMixin(LoginRequiredMixin):
    """Возвращает сниппет, если пользователь является его владельцем."""

    permission_denied_message = "Доступ разрешен только владельцу."

    def get_object(self):
        snippet = get_object_or_404(Snippet.active, url=self.kwargs["url"])
        if snippet.owner != self.request.user:
            return self.handle_no_permission()
        return snippet
