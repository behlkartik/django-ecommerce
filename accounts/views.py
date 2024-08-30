from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('home')) 
    form = AuthenticationForm(request)
    context = {"form": form}
    return render(request, 'accounts/login.html', context=context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect(reverse('home'))

def register_view(request):
    form = UserCreationForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()
        return redirect(reverse('login'))
    return render(request, 'accounts/register.html', context=context)


def change_password_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    form = PasswordChangeForm(request.user, data=request.POST)
    context = {"form": form}
    if form.is_valid():
        form.save()
        return redirect(reverse('home')) 
    print(form.data)
    return render(request, 'accounts/changepass.html', context=context)