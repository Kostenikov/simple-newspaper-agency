from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from core.forms import NewspaperForm, SearchForm
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


class TopicCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_message = "Topic was successfully created!"

    def get_success_url(self):
        return reverse_lazy("core:topic-detail", kwargs={"pk": self.object.pk})


class TopicUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_message = "Topic was successfully updated!"

    def get_success_url(self):
        return reverse_lazy("core:topic-detail", kwargs={"pk": self.object.pk})


class TopicDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("core:topic-list")
    success_message = "Topic was successfully deleted!"


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


class NewspaperCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_message = "Newspaper was successfully created!"

    def get_success_url(self):
        return reverse_lazy("core:newspaper-detail", kwargs={"pk": self.object.pk})


class NewspaperUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_message = "Newspaper was successfully updated!"

    def get_success_url(self):
        return reverse_lazy("core:newspaper-detail", kwargs={"pk": self.object.pk})


class NewspaperDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("core:newspaper-list")
    success_message = "Newspaper was successfully deleted!"
