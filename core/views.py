from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from core.forms import NewspaperForm, SearchForm, RedactorCreationForm, RedactorUpdateForm
from core.models import Topic, Newspaper

Redactor = get_user_model()


class HomeView(generic.TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = {
            "topics_count": Topic.objects.count(),
            "newspapers_count": Newspaper.objects.count(),
            "redactors_count": Redactor.objects.count(),
        }
        return context


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        context["search_form"] = SearchForm(
            initial={"query": query}
        )
        return context

    def get_queryset(self):
        queryset = Topic.objects.all()
        form = SearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["query"])

        return queryset


class TopicDetailView(LoginRequiredMixin, generic.DetailView):
    model = Topic
    queryset = Topic.objects.prefetch_related("newspapers")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic_news_count"] = self.object.newspapers.count()
        return context


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("core:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("core:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("core:topic-list")


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        context["search_form"] = SearchForm(
            initial={"query": query}
        )
        return context

    def get_queryset(self):
        queryset = Newspaper.objects.select_related("topic")
        form = SearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                Q(title__icontains=form.cleaned_data["query"]) |
                Q(topic__name__icontains=form.cleaned_data["query"])
            )

        return queryset


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper
    queryset = Newspaper.objects.select_related("topic").prefetch_related("publishers")


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("core:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("core:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("core:newspaper-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    template_name = "core/redactor_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        context["search_form"] = SearchForm(
            initial={"query": query}
        )
        return context

    def get_queryset(self):
        queryset = Redactor.objects.all()
        form = SearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                Q(first_name__icontains=form.cleaned_data["query"]) |
                Q(last_name__icontains=form.cleaned_data["query"]) |
                Q(email__icontains=form.cleaned_data["query"])
            )

        return queryset


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    template_name = "core/redactor_detail.html"
    queryset = Redactor.objects.prefetch_related("newspapers__topic")


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    template_name = "core/redactor_form.html"
    success_url = reverse_lazy("core:redactor-list")


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorUpdateForm
    template_name = "core/redactor_form.html"
    success_url = reverse_lazy("core:redactor-list")


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    template_name = "core/redactor_confirm_delete.html"
    success_url = reverse_lazy("core:redactor-list")
