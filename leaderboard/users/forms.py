# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignupForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Choose a username", "class": "form-control"}
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your email", "class": "form-control"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm Password", "class": "form-control"}
        )
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords do not match")
        return confirm_password


class Signinform(forms.models.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your email", "class": "form-control"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password", "class": "form-control"}
        )
    )

    class Meta:
        model = User
        fields = ["username", "password"]