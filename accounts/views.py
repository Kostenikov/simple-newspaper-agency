from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import SearchForm, RedactorCreationForm, RedactorUpdateForm

Redactor = get_user_model()


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
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
    queryset = Redactor.objects.prefetch_related("newspapers__topic")


class RedactorCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    success_message = "Redactor was successfully created!"

    def get_success_url(self):
        return reverse_lazy("accounts:redactor-detail", kwargs={"pk": self.object.pk})


class RedactorUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorUpdateForm
    success_message = "Redactor was successfully updated!"

    def get_success_url(self):
        return reverse_lazy("accounts:redactor-detail", kwargs={"pk": self.object.pk})


class RedactorDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("accounts:redactor-list")
    success_message = "Redactor was successfully deleted!"


class RedactorPasswordChange(SuccessMessageMixin, PasswordChangeView):
    model = Redactor
    form_class = PasswordChangeForm
    success_message = "Password was successfully changed!"

    def get_success_url(self):
        return reverse_lazy("accounts:redactor-detail", kwargs={"pk": self.kwargs["pk"]})
