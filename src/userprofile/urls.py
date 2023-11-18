from django.urls import path

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)

from . import views


urlpatterns = [
    path("login/", views.loginuser, name="login"),
    path("logout/", views.logoutuser, name="logout"),
    path("register/", views.register, name="register"),
    path("userprofile/", views.userprofile, name="userprofile"),
    path("otherprofile/<int:id>/", views.otherprofile, name="otherprofile"),
    path("userprofilecreate/", views.userprofilecreate, name="userprofilecreate"),
    path("change_password/", views.change_password, name="change_password"),
    path(
        "reset/password/",
        PasswordResetView.as_view(template_name="userprofile/pass_reset.html"),
        name="password_reset",
    ),
    path(
        "reset/password/done/",
        PasswordResetDoneView.as_view(template_name="userprofile/pass_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="userprofile/pass_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetView.as_view(template_name="userprofile/pass_reset_complete.html"),
        name="password_reset_complete",
    ),
]
