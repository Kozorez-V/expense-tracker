from datetime import date

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView
from django.db.models import Sum, Max, Min, Count
from django.db.models.functions import ExtractIsoWeekDay, ExtractWeek

from .forms import *


def index(request):
    context = {
        'title': 'Главная страница'
    }
    return render(request, 'expense_tracker/index.html', context)


def statistics(request):
    context = {
        'title': 'Статистика'
    }

    return render(request, 'expense_tracker/statistics.html', context)


class TodayStatistics(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'expense_tracker/today_statistics.html'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today_expenses = Expense.objects.filter(date=date.today(), user=self.request.user)

        context['category_total'] = today_expenses.values('category').annotate(total_amount=Sum('amount', default=0.0))
        context['category_total_pk'] = context['category_total'].values_list('category', flat=True)

        context['total'] = today_expenses.aggregate(Sum('amount', default=0.0))
        context['max_amount'] = today_expenses.aggregate(Max('amount', default=0.0))
        context['min_amount'] = today_expenses.aggregate(Min('amount', default=0.0))

        context['title'] = 'Статистика'

        return context


class WeekStatistics(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'expense_tracker/week_statistics.html'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_week_expenses = Expense.objects.filter(date__week=date.today().isocalendar()[1],
                                                       user=self.request.user)

        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

        context['category_total'] = current_week_expenses.values('category') \
            .annotate(total_amount=Sum('amount', default=0.0))
        context['category_total_pk'] = context['category_total'].values_list('category', flat=True)

        context['total'] = current_week_expenses.aggregate(Sum('amount', default=0.0))
        context['max_amount'] = current_week_expenses.aggregate(Max('amount', default=0.0))
        context['min_amount'] = current_week_expenses.aggregate(Min('amount', default=0.0))

        expenses_by_weekday = current_week_expenses.values('category', 'date') \
            .annotate(weekday=ExtractIsoWeekDay('date')).annotate(Sum('amount'))

        weekday_total = {}

        for number in range(len(days)):
            weekday_total[days[number]] = {}
            for category in context['categories']:
                for exp in expenses_by_weekday:
                    if exp['category'] == category.pk:
                        if exp['weekday'] == number + 1:
                            weekday_total[days[number]][category.name] = exp['amount__sum']

        # for weekday, expense in weekday_total.items():
        #     print(weekday)
        #     for category, amount in expense.items():
        #         print(f'Категория: {category} \n Сумма: {amount}')

        context['table_headers'] = list(weekday_total)

        print(weekday_total)
        context['weekday_total'] = weekday_total
        context['title'] = 'Еженедельная статистика'

        return context


class ShowCategories(ListView):
    paginate_by = 10
    model = Category
    context_object_name = 'categories'
    template_name = 'expense_tracker/category_list.html'

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
        return Expense.objects.filter(user=self.request.user).select_related('category')


def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            try:
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                return redirect('categories')
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
                return redirect('categories')
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
        return redirect('categories')

    context = {
        'title': 'Удаление категории',
        'category': category.name,
        'category_pk': category.pk,
        'expenses': expenses
    }

    return render(request, 'expense_tracker/delete_category.html', context)


def transfer_expenses(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    expenses = Expense.objects.filter(category=category)

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
