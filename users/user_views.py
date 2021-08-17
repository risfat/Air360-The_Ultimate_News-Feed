from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from Air360 import settings
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail


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
                email = form.cleaned_data.get('email')

                messages.success(req, 'Account was created successfully for ' + user)

                subject = 'Warm Welcome To Air360'
                message = f'Hi {user}, Thank you for registering in Air360. Enjoy Your Stay. '
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email, ]
                send_mail(subject, message, email_from, recipient_list)

                return redirect('login')

        context = {'form': form}

        return render(req, 'register.html', context)


def logout_user(req):
    logout(req)
    return redirect('login')

