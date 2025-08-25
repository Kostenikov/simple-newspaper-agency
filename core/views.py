from django.contrib.auth import get_user_model
from django.views import generic

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


class TopicListView(generic.ListView):
    model = Topic


class NewspaperListView(generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.select_related("topic")
    paginate_by = 10


class RedactorListView(generic.ListView):
    model = Redactor
    template_name = "core/redactor_list.html"
