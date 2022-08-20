from datetime import date

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView
from django.db.models import Sum, Max, Min, Count
from django.db.models.functions import ExtractIsoWeekDay, ExtractMonth

from .forms import *


def index(request):
    context = {
        'title': 'Главная страница'
    }
    return render(request, 'expense_tracker/index.html', context)


class TodayStatistics(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'expense_tracker/today_statistics.html'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).only('name')

    def get_today_expenses(self):
        return Expense.objects.filter(date=date.today(), user=self.request.user)

    def get_category_calculation(self):
        today_expenses = self.get_today_expenses()

        amount_per_category = today_expenses.values('category') \
            .annotate(total_amount=Sum('amount', default=0.0))
        nonempty_category_pk = amount_per_category.values_list('category', flat=True)

        total = today_expenses.aggregate(Sum('amount', default=0.0))
        max_amount = today_expenses.aggregate(Max('amount', default=0.0))
        min_amount = today_expenses.aggregate(Min('amount', default=0.0))

        return amount_per_category, nonempty_category_pk, total, max_amount, min_amount

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['amount_per_category'], context['nonempty_category_pk'], context['total'], \
        context['max_amount'], context['min_amount'] = self.get_category_calculation()

        context['title'] = 'Статистика'

        return context


class WeeklyStatistics(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'expense_tracker/week_statistics.html'

    def get_current_week_expenses(self):
        return Expense.objects.filter(date__week=date.today().isocalendar()[1],
                                      user=self.request.user)

    def get_category_calculation(self):
        current_week_expenses = self.get_current_week_expenses()
        amount_per_category = current_week_expenses.values('category') \
            .annotate(total_amount=Sum('amount', default=0.0))
        nonempty_category_pk = amount_per_category.values_list('category', flat=True)
        total = current_week_expenses.aggregate(Sum('amount', default=0.0))
        max_amount = current_week_expenses.aggregate(Max('amount', default=0.0))
        min_amount = current_week_expenses.aggregate(Min('amount', default=0.0))

        return amount_per_category, nonempty_category_pk, total, max_amount, min_amount

    def get_weekday_total(self):
        categories = Category.objects.filter(user=self.request.user)

        current_week_expenses = self.get_current_week_expenses()
        expenses_by_weekday = current_week_expenses.values('category', 'date') \
            .annotate(weekday=ExtractIsoWeekDay('date')).annotate(Sum('amount'))

        weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

        weekday_total = {}

        for number in range(len(weekdays)):
            weekday_total[weekdays[number]] = {}
            for category in categories:
                for exp in expenses_by_weekday:
                    if exp['category'] == category.pk:
                        if exp['weekday'] == number + 1:
                            weekday_total[weekdays[number]][category.name] = exp['amount__sum']

        return categories, weekdays, weekday_total

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['amount_per_category'], context['nonempty_category_pk'], context['total'], \
        context['max_amount'], context['min_amount'] = self.get_category_calculation()

        context['categories'], context['weekdays'], context['weekday_total'] = self.get_weekday_total()

        context['title'] = 'Статистика'

        return context


class AnnualStatistics(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'expense_tracker/annual_statistics.html'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).only('name')

    def get_current_year_expenses(self):
        return Expense.objects.filter(date__year=date.today().isocalendar()[0],
                                                       user=self.request.user)

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year_expenses = Expense.objects.filter(date__year=date.today().isocalendar()[0],
                                                       user=self.request.user)

        context['amount_per_category'] = current_year_expenses.values('category') \
            .annotate(total_amount=Sum('amount', default=0.0))
        context['nonempty_category_pk'] = context['amount_per_category'].values_list('category', flat=True)

        context['total'] = current_year_expenses.aggregate(Sum('amount', default=0.0))
        context['max_amount'] = current_year_expenses.aggregate(Max('amount', default=0.0))
        context['min_amount'] = current_year_expenses.aggregate(Min('amount', default=0.0))

        expenses_by_month = current_year_expenses.values('category') \
            .annotate(month=ExtractMonth('date')).values('category', 'month').annotate(Sum('amount'))

        months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                  'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

        month_total = {}

        for number in range(len(months)):
            month_total[months[number]] = {}
            for category in context['categories']:
                for exp in expenses_by_month:
                    if exp['category'] == category.pk:
                        if exp['month'] == number + 1:
                            month_total[months[number]][category.name] = exp['amount__sum']

        context['month_total'] = month_total
        context['months'] = months
        context['title'] = 'Статистика'

        return context


class ShowCategories(LoginRequiredMixin, ListView):
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


class ExpenseHistory(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Expense
    context_object_name = 'expenses'
    template_name = 'expense_tracker/expense_history.html'

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'История расходов'
        return context


class ShowProfile(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'expense_tracker/profile.html'


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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
        'title': 'Учет расходов',
        'button': 'Добавить'
    }

    return render(request, 'expense_tracker/add_expense.html', context)


@login_required
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


@login_required
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'expense_tracker/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context


def logout_user(request):
    logout(request)
    return redirect('login')
