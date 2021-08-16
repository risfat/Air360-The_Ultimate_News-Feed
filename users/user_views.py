from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def login_page(req):
    if req.user.is_authenticated:
        return redirect('home')
    else:
        if req.method == 'POST':
            username = req.POST.get('username')
            password = req.POST.get('password')

            user = authenticate(req, username=username, password=password)

            if user is not None:
                login(req, user)
                return redirect('home')

            else:
                messages.info(req, 'Username or Password is Incorrect')

        context = {}
        return render(req, 'login.html', context)


def register_page(req):
    if req.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if req.method == 'POST':
            form = CreateUserForm(req.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(req, 'Account was created successfully for ' + user)
                return redirect('login')

        context = {'form': form}

        return render(req, 'register.html', context)


def logout_user(req):
    logout(req)
    return redirect('login')

