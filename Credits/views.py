from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import TestDBUser
from .forms import UserForm


@login_required
def index(request):
    return render(request, 'credits/index.html')


def registration(request):
    if request.method == 'POST':
        if request.POST.get('password_confirm') == None:
            print('Вход')
            user_form = UserForm()
            user = authenticate(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
            )
            if user:
                login(request, user)
                return redirect('main')
            return render(request, 'credits/registration.html', {'user_form': user_form, 'invalid': True})
        else:
            print('Регистрация')
            user_form = UserForm(request.POST)  # регистрация
            if user_form.is_valid():
                user = user_form.save()
                login(request, user)
                return redirect('main')
            return render(request, 'credits/registration.html', {'user_form': user_form})

    user_form = UserForm()
    return render(request, 'credits/registration.html', {'user_form': user_form})


def guide(request):
    return render(request, 'credits/tytorial.html', {'username': request.user})


def soon(request):
    return render(request, 'credits/soon.html')


def user_logout(request):
    logout(request)
    return redirect('login')

# -------- TEST ---------

def test_login_register(request):
    if request.method == 'POST':
        if request.POST.get('password_confirm') == None:
            print('Вход')
            user_form = UserForm()
            user = authenticate(
                username=request.POST.get('username'),
                password=request.POST.get('password'),
            )
            if user:
                login(request, user)
                return redirect('test_index')
            return render(request, 'credits/test_login_register.html', {'user_form': user_form, 'invalid': True})
        else:
            print('Регистрация')
            user_form = UserForm(request.POST) # регистрация
            if user_form.is_valid():
                user = user_form.save()
                login(request, user)
                return redirect('test_index')
            return render(request, 'credits/test_login_register.html', {'user_form': user_form})

    user_form = UserForm()
    return render(request, 'credits/test_login_register.html', {'user_form': user_form})

def test_index(request):
    return render(request, 'credits/test_index.html')