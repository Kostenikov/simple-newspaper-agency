from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from core.forms import NewspaperForm
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
    queryset = Newspaper.objects.select_related("topic")
    paginate_by = 10


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


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    template_name = "core/redactor_detail.html"
    queryset = Redactor.objects.prefetch_related("newspapers__topic")
