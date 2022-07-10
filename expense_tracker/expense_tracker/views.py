from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView

from .forms import *


def index(request):
    return render(request, 'expense_tracker/index.html', {'title': 'Главная страница'})


def settings(request):
    categories = Category.objects.filter(user=request.user)

    return render(request, 'expense_tracker/settings.html', {'title': 'Настройки', 'categories': categories})


def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            try:
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                return redirect('settings')
            except:
                form.add_error(None, 'Ошибка добавления категории')
    else:
        form = AddCategoryForm()

    return render(request, 'expense_tracker/category_form.html', {'form': form,
                                                                  'title': 'Добавить категорию',
                                                                  'button': 'Добавить'})


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, instance=category)
        if form.is_valid():
            try:
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                return redirect('settings')
            except:
                form.add_error(None, 'Ошибка редактирования категории')
    else:
        form = AddCategoryForm(instance=category)

    return render(request, 'expense_tracker/category_form.html', {'form': form,
                                                                  'title': 'Редактировать категорию',
                                                                  'button': 'Изменить'})


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if Expense.objects.filter(category=category).exists():
        print('Oops')
    else:
        category.delete()

    return redirect('settings')


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
