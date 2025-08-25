from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from core.models import Newspaper, Topic

Redactor = get_user_model()


class NewspaperForm(forms.ModelForm):
    title = forms.CharField(max_length=255)
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all()
    )
    published_date = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control"
            },
            format="%Y-%m-%dT%H:%M"
        ),
        input_formats=["%Y-%m-%dT%H:%M"]
    )
    publishers = forms.ModelMultipleChoiceField(
        queryset=Redactor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": "3",
            }
        )
    )

    class Meta:
        model = Newspaper
        fields = "__all__"


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Input something..."})
    )


class RedactorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
        )


class RedactorUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = Redactor
        fields = (
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
        )
