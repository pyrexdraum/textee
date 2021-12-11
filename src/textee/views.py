from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView

from .models import Snippet
from .forms import SnippetForm
from .service import highlight_code


class SnippetCreateView(CreateView):
    model = Snippet
    form_class = SnippetForm
    template_name = "textee/index.html"

    def form_valid(self, form):
        snippet = form.save(commit=False)
        is_user = self.request.user.is_authenticated
        snippet.owner = self.request.user if is_user else None
        snippet.save()
        return redirect(snippet)


class SnippetDetailView(DetailView):
    queryset = Snippet.active.all()
    slug_field = "url"
    slug_url_kwarg = "url"
    context_object_name = "snippet"
    template_name = "textee/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        snippet = self.get_object()
        if snippet.syntax:
            context["highlighted_code"] = highlight_code(snippet.code, snippet.syntax)
        return context
