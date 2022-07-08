from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .forms import *


def index(request):
    return render(request, 'expense_tracker/index.html', {'title': 'Главная страница'})


def add_expense(request):
    if request.method == 'POST':
        form = AddExpenseForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('add_expense')
            except:
                form.add_error(None, 'Ошибка внесения расходов')
    else:
        form = AddExpenseForm()

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