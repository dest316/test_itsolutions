from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm


def reg(request):
    # Обработка формы регистрации пользователя
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    # Отображение пустой формы регистрации в случае GET-запроса
    else:
        form = RegisterForm()
    return render(request, 'users/reg.html', {'form': form})


def log_on(request):
    # Обработка формы авторизации пользователя
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        # Если введены корректные данные и пользователь с такими данными существует - производим авторизацию
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    # Отображение пустой формы регистрации в случае GET-запроса
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


# Обработка выхода из профиля пользователем
def log_out(request):
    logout(request)
    return redirect('/')
