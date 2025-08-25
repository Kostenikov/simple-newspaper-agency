from django.urls import path

from core.views import HomeView, TopicListView, NewspaperListView, RedactorListView

app_name = "core"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
]
