# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from .forms import SignupForm, Signinform, ForgotpwdForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from . import mail as mail


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
            # us = mail.Mail()
            # us.send(
            #     to=email,
            #     message=f"Subject: Welcome to GDGOC! \n\n Hello {username},\n\nThank you for joining Google Developer Groups on Campus ! We're excited to have you onboard with us .\n\nBest Regards,\nGDGOC Team",
            # )
            # print("Email sent!")

            # Show success message and redirect to login page
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
            email = form.cleaned_data["email"]  # Using email as username field
            password = form.cleaned_data["password"]
            # print(email, password)

            # Try to get the user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Invalid email address.")
                return render(request, "user_temp/login.html", {"form": form})

            # Authenticate user with email and password
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, "Login successful!")
                return redirect(
                    "leaderboard"
                )  # Redirect to the desired page after successful login
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
            email = form.cleaned_data["email"]  # Using email as username field
            print(email)
        else:
            messages.error(
                request, "There was an error with your form. Please try again."
            )
            return render(request, "user_temp/login.html", {"form": form})

    else:
        form = ForgotpwdForm()

    return render(request, "user_temp/forgot.html", {"form": form})
