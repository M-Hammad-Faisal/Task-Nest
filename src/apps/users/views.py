from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Team
from django.utils.crypto import get_random_string


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("dashboard")
        messages.error(request, form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, "users/auth.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("dashboard")
        messages.error(request, form.errors)
    else:
        form = AuthenticationForm()
    return render(request, "users/auth.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


@login_required(login_url="login")
def team_create(request):
    if request.method == "POST":
        team_name = request.POST.get("name")
        if team_name:
            team = Team.objects.create(
                name=team_name,
                owner=request.user,
                invite_code=get_random_string(
                    8, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                ),
            )
            team.members.add(request.user)
            messages.success(request, f"Team '{team.name}' created successfully!")
            return redirect("team_list")
    return render(request, "teams/team_create.html")


@login_required(login_url="login")
def team_list(request):
    teams = request.user.teams.all()
    return render(request, "teams/team_list.html", {"teams": teams})


@login_required(login_url="login")
def team_join(request):
    if request.method == "POST":
        invite_code = request.POST.get("invite_code")
        try:
            team = Team.objects.get(invite_code=invite_code)
            team.members.add(request.user)
            messages.success(request, f"Joined team '{team.name}' successfully!")
            return redirect("team_list")
        except Team.DoesNotExist:
            messages.error(request, "Invalid invite code.")
    return render(request, "teams/team_join.html")


@login_required(login_url="login")
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "users/profile.html", {"user": request.user, "form": form})
