from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomPasswordResetCompleteView, profile

urlpatterns = [
    # Other URLs
    path("signup/", views.signup, name="signup"),
    path("", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("forgot/", views.forgotpwd, name="forgotpwd"),
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("profile/", profile, name="user_profile"),
]
