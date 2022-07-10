from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView

from .forms import *


def index(request):
    return render(request, 'expense_tracker/index.html', {'title': 'Главная страница'})

def settings(request):
    return render(request, 'expense_tracker/settings.html', {'title': 'Настройки'})


def add_expense(request):
    if request.method == 'POST':
        form = AddExpenseForm(data=request.POST, request=request)
        if form.is_valid():
            try:
                expense = form.save(commit=False)
                expense.user = request.user
                expense.save()
                return redirect('add_expense')
            except:
                form.add_error(None, 'Ошибка внесения расходов')
    else:
        form = AddExpenseForm(request=request)

    return render(request, 'expense_tracker/add_expense.html', {'form': form, 'title': 'Внести расходы'})


class SignUpUser(CreateView):
    form_class = SignUpForm
    template_name = 'expense_tracker/sign_up.html'
    success_url = 'login'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'expense_tracker/login.html'


def logout_user(request):
    logout(request)
    return redirect('login')