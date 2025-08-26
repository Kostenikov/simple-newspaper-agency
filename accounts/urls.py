from django.urls import path

from accounts.views import (
    RedactorListView,
    RedactorDetailView,
    RedactorCreateView,
    RedactorUpdateView,
    RedactorDeleteView,
    RedactorPasswordChange,
)

app_name = "accounts"
urlpatterns = [
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path("redactors/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"),
    path("redactors/create/", RedactorCreateView.as_view(), name="redactor-create"),
    path("redactors/<int:pk>/update/", RedactorUpdateView.as_view(), name="redactor-update"),
    path("redactors/<int:pk>/delete/", RedactorDeleteView.as_view(), name="redactor-delete"),
    path("redactors/<int:pk>/change-password/", RedactorPasswordChange.as_view(), name="redactor-password-change"),
]
