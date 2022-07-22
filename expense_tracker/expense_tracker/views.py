from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView

from .forms import *


def index(request):
    context = {
        'title': 'Главная страница'
    }
    return render(request, 'expense_tracker/index.html', context)


def statistics(request):
    return render(request, 'expense_tracker/statistics.html')


class ShowCategories(ListView):
    paginate_by = 10
    model = Category
    context_object_name = 'categories'
    template_name = 'expense_tracker/settings.html'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        return context


class ExpenseHistory(ListView):
    paginate_by = 10
    model = Expense
    context_object_name = 'expenses'
    template_name = 'expense_tracker/expense_history.html'

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


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

    context = {
        'form': form,
        'title': 'Добавить категорию',
        'button': 'Добавить'
    }

    return render(request, 'expense_tracker/category_form.html', context)


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

    context = {
        'form': form,
        'title': 'Редактировать категорию',
        'button': 'Изменить'
    }

    return render(request, 'expense_tracker/category_form.html', context)


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    expenses = Expense.objects.filter(category=category)

    if expenses.exists():
        messages.warning(request, f'Категория {category.name} содержит расходы')
    else:
        messages.info(request, f'Категория {category.name} пуста')

    if request.method == 'POST':
        category.delete()
        return redirect('settings')

    context = {
        'title': 'Удаление категории',
        'category': category.name,
        'category_pk': category.pk,
        'expenses': expenses
    }

    return render(request, 'expense_tracker/delete_category.html', context)


def transfer_expenses(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)  # миксин
    expenses = Expense.objects.filter(category=category)  # миксин

    if request.method == 'POST':
        form = RestrictedExpenseForm(data=request.POST, request=request)
        if form.is_valid():
            category_user = form.cleaned_data.get('category')
            for expense in expenses:
                expense.category = category_user
                expense.user = request.user
                expense.save()
            return redirect('delete_category', pk=category_pk)
    else:
        form = RestrictedExpenseForm(request=request)

    context = {
        'form': form,
        'title': 'Перенести расходы',
        'button': 'Изменить'
    }

    return render(request, 'expense_tracker/transfer_expenses.html', context)


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

    context = {
        'form': form,
        'title': 'Внести расходы',
        'button': 'Добавить'
    }

    return render(request, 'expense_tracker/add_expense.html', context)


def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = AddExpenseForm(request.POST, request=request, instance=expense)
        if form.is_valid():
            try:
                expense = form.save(commit=False)
                expense.user = request.user
                expense.save()
                return redirect('add_expense')
            except:
                form.add_error(None, 'Ошибка редактирования расходов')
    else:
        form = AddExpenseForm(request=request, instance=expense)

    context = {
        'form': form,
        'title': 'Редактировать запись расхода',
        'button': 'Изменить'
    }

    return render(request, 'expense_tracker/add_expense.html', context)


def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()

    return redirect('add_expense')


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