from django.views.generic import CreateView, DetailView, UpdateView, View
from django.views.generic.edit import DeletionMixin

from .forms import SnippetForm
from .mixins import OwnerSnippetRequiredMixin
from .models import Snippet
from .service import highlight_code


class SnippetCreateView(CreateView):
    model = Snippet
    form_class = SnippetForm
    template_name = "textee/index.html"

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.owner = self.request.user
        return super().form_valid(form)


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


class SnippetDeleteView(OwnerSnippetRequiredMixin, DeletionMixin, View):
    def get_success_url(self):
        return self.request.user.get_absolute_url()


class SnippetUpdateView(OwnerSnippetRequiredMixin, UpdateView):
    form_class = SnippetForm
    template_name = "textee/snippet_edit.html"
