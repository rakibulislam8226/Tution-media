from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.loader import render_to_string


from .forms import SignUpForm, UserProfileForm
from .models import UserProfile


# Create your views here.
def loginuser(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successfully.")
                return redirect("home")
            else:
                messages.info(request, "Invalid username or password.")
        else:
            messages.info(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "userprofile/login.html", {"form": form})


def logoutuser(request):
    logout(request)
    messages.success(request, "Logout successfully.")
    return redirect("/")


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            mail_subject = "An account created"
            messages = render_to_string(
                "userprofile/account.html",
                {"user": user, "domain": current_site.domain},
            )
            send_mail = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, messages, to=[send_mail])
            email.send()
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request, "userprofile/signup.html", {"form": form})


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            update_session_auth_hash(request, form.user)
            form.save()
            messages.success(request, "User password successfully changed.")
            return redirect("login")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "userprofile/pass_change.html", {"form": form})


def userprofilecreate(request):
    try:
        instance = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        instance = None
    if request.method == "POST":
        if instance:
            form = UserProfileForm(request.POST, request.FILES, instance=instance)
        else:
            form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "Profile Edited Successfully.")
            return redirect("userprofile")
    else:
        form = UserProfileForm(instance=instance)
    return render(request, "userprofile/userprofilecreate.html", {"form": form})


def userprofile(request):
    user = request.user
    return render(request, "userprofile/userprofile.html", {"user": user})


def otherprofile(request, id):
    user = User.objects.get(id=id)
    return render(request, "userprofile/otherprofile.html", {"user": user})
