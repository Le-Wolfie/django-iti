from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.validators import RegexValidator

from .models import CustomUser, Project


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True, max_length=50, help_text="Required. Your first name.",
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
    )
    last_name = forms.CharField(
        required=True, max_length=50, help_text="Required. Your last name.",
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
    )
    email = forms.EmailField(
        required=True, help_text="Required. Enter a valid email address.",
        widget=forms.EmailInput(attrs={"autocomplete": "off"}),
    )
    mobile = forms.CharField(
        required=True,
        max_length=11,
        validators=[
            RegexValidator(
                regex=r"^\d{11}$",
                message="Mobile number must be 11 digits long.",
            )
        ],
        widget=forms.TextInput(
            attrs={"type": "tel", "pattern": "[0-9]*"}),
        help_text="Required. Your 11-digit mobile number.",
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email",
                  "password1", "password2", "mobile"]


class ChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ["title", "details", "target", "start_time", "end_time"]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
