# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import (
    SignupForm,
    Signinform,
    ForgotpwdForm,
    ProfileForm,
    ProfilePictureForm,
)
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import views as auth_views  # Ensure this import is included
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import Profile
import json
from django.conf import settings
from social_django.utils import load_strategy, load_backend
from social_core.actions import do_auth
from social_core.backends.github import GithubOAuth2
from social_core.exceptions import AuthException, AuthForbidden


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            if (
                User.objects.filter(username=username).exists()
                or User.objects.filter(email=email).exists()
            ):
                messages.error(request, "Username or email already taken.")
                return render(request, "user_temp/signup.html", {"form": form})

            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.email = email
            user.save()
            send_mail(
                from_email="pradeepkalyan1275@gmail.com",
                fail_silently=False,
                subject="Welcome to GDGOC!",
                recipient_list=[email],
                message=f"Subject: Welcome to GDGOC! \n\n Hello {username},\n\nThank you for joining Google Developer Groups on Campus ! We're excited to have you onboard with us .\n\nBest Regards,\nGDGOC Team",
            )

            messages.success(
                request, "Account created successfully! A welcome email has been sent."
            )
            return redirect("login")

        else:
            messages.error(request, "There was an error with your form.")
            return render(
                request, "user_temp/signup.html", {"form": form, "errors": form.errors}
            )

    else:
        form = SignupForm()
    return render(request, "user_temp/signup.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = Signinform(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Invalid email address.")
                return render(request, "user_temp/login.html", {"form": form})

            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, "Login successful!")
                return redirect("leaderboard")
            else:
                messages.error(request, "Invalid email or password.")
                return render(request, "user_temp/login.html", {"form": form})

        else:
            messages.error(
                request, "There was an error with your form. Please try again."
            )
            return render(request, "user_temp/login.html", {"form": form})

    else:
        form = Signinform()

    return render(request, "user_temp/login.html", {"form": form})


def logout(request):
    auth_logout(request)
    return redirect("/")


def forgotpwd(request):
    if request.method == "POST":
        form = ForgotpwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
                current_site = get_current_site(request)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = f"{request.scheme}://{current_site.domain}/users/reset/{uid}/{token}/"

                subject = "Password Reset Request"
                message = (
                    f"Subject: {subject}\n\n"
                    f"Hello {user.username},\n\n"
                    f"We received a request to reset your password. If you did not make this request, "
                    f"please ignore this email.\n\n"
                    f"To reset your password, click the link below:\n"
                    f"{reset_link}\n\n"
                    f"Thank you!"
                )
                send_mail(
                    subject,
                    message,
                    "noreply@example.com",
                    [email],
                    fail_silently=False,
                )
                messages.success(
                    request, "Password reset link has been sent to your email."
                )
            except User.DoesNotExist:
                messages.error(
                    request, "No user found with the provided email address."
                )
        else:
            messages.error(request, "Invalid form submission. Please try again.")
    else:
        form = ForgotpwdForm()

    return render(request, "user_temp/forgot.html", {"form": form})


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    def get_redirect_url(self):
        return reverse_lazy("users/")


from django.shortcuts import render, redirect
from .forms import ProfileForm, ProfilePictureForm
from django.contrib.auth.decorators import login_required
from .models import Profile


@login_required
def profile(request):
    profile = request.user.profile

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=profile)
        picture_form = ProfilePictureForm(request.POST, request.FILES, instance=profile)

        if profile_form.is_valid() and picture_form.is_valid():
            # Save profile form
            profile_form.save()

            # Handle profile picture update if there is a new picture
            profile_picture = picture_form.cleaned_data.get("profile_picture")
            if profile_picture:
                profile.profile_picture = profile_picture
                profile.save()

            # Update user's first and last name
            request.user.first_name = profile_form.cleaned_data.get("first_name")
            request.user.last_name = profile_form.cleaned_data.get("last_name")
            request.user.save()

            return redirect("user_profile")

    else:
        profile_form = ProfileForm(instance=profile)
        picture_form = ProfilePictureForm(instance=profile)

    return render(
        request,
        "user_temp/profile.html",
        {
            "profile_form": profile_form,
            "picture_form": picture_form,
            "profile": profile,
        },
    )

def github_login(request):
    strategy = load_strategy(request)
    backend = GithubOAuth2(strategy=strategy)

    try:
        # Perform authentication via GitHub
        user = backend.do_auth(request.GET.get("code"))
    except AuthException as e:
        messages.error(request, f"GitHub authentication failed: {e}")
        return redirect("login")

    if user:
        # Fetch GitHub email
        github_email = user.email

        # Check if the email matches an existing user
        existing_user = User.objects.filter(email=github_email).first()
        if existing_user:
            # Merge accounts by linking GitHub with the existing user
            if user != existing_user:
                user.delete()  # Delete the duplicate account
                backend.associate(existing_user)  # Link GitHub to the existing account
                user = existing_user

            messages.success(request, "Your GitHub account has been linked successfully!")
        else:
            messages.success(request, "GitHub account authenticated successfully!")

        auth_login(request, user)
        return redirect("leaderboard")
    else:
        messages.error(request, "GitHub login failed.")
        return redirect("login")

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=profile)

        if profile_form.is_valid():
            profile_form.save()

            # Optionally, add logic to link GitHub
            if 'github_link' in request.POST:
                github_link = request.POST.get('github_link')
                if github_link:
                    strategy = load_strategy(request)
                    backend = GithubOAuth2(strategy=strategy)
                    try:
                        github_user = backend.do_auth(request.POST.get("code"))
                        if github_user:
                            profile.github_account = github_user.username
                            profile.save()
                            messages.success(request, "GitHub account linked successfully!")
                    except AuthException as e:
                        messages.error(request, f"GitHub linking failed: {e}")

            messages.success(request, "Profile updated successfully!")
            return redirect("edit_profile")

    else:
        profile_form = ProfileForm(instance=profile)
    return render(request, "user_temp/edit_profile.html", {"profile_form": profile_form, "profile": profile})

# Ensure that the Profile model has a field for GitHub account, e.g., github_account = models.CharField(max_length=255, blank=True)

# Add GitHub login URL generator to templates
# In the templates like login.html or edit_profile.html, use {% provider_login_url 'github' %} to create GitHub login links.
