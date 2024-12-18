# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


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
        fields = ["email", "password"]


class ForgotpwdForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your email ", "class": "form-control"}
        )
    )

    class Meta:
        model = User
        fields = ["email"]


from django import forms
from django.contrib.auth.models import User


from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "github", "linkedin", "first_name", "last_name"]
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tell us about yourself",
                }
            ),
            "github": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your GitHub URL",
                }
            ),
            "linkedin": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your LinkedIn URL",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your first name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your last name",
                }
            ),
        }


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_picture"]
        widgets = {
            "profile_picture": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }
