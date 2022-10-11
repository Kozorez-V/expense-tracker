from datetime import date, datetime

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView

from ..models import Category, Expense
from ..servers import get_weekday_total, get_month_total
from ..mixins import StatisticsContextMixin


class TodayStatistics(LoginRequiredMixin, StatisticsContextMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'expense_tracker/today_statistics.html'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).only('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        expenses = Expense.objects.today(self.request.user)
        selected_date = None

        if self.request.method == 'GET' and self.request.GET.get('select_date') is not None:
            selected_date = datetime.strptime(self.request.GET.get('select_date'), '%Y-%m-%d').date()
            expenses = Expense.objects.filter(
                date=selected_date,
                user=self.request.user
                )

        c_def = self.get_user_context(
            expenses=expenses,
            title='День',
            selected_date=selected_date,
            limit_time='day_limit'
            )
            
        return dict(list(context.items()) + list(c_def.items()))


class MonthStatistics(LoginRequiredMixin, StatisticsContextMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'expense_tracker/month_statistics.html'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).only('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        month_expenses = Expense.objects.current_month(self.request.user)

        selected_date = None

        if self.request.method == 'GET' and self.request.GET.get('select_date') is not None:
            selected_date = datetime.strptime(self.request.GET.get('select_date'), '%Y-%m-%d').date()
            month_expenses = Expense.objects.filter(
                date__month=selected_date.month,
                user=self.request.user
                )

        c_def = self.get_user_context(
            expenses=month_expenses,
            selected_date=selected_date,
            title='Месяц',
            limit_time='month_limit'
            )

        return dict(list(context.items()) + list(c_def.items()))


class WeeklyStatistics(LoginRequiredMixin, StatisticsContextMixin, ListView):
    model = Category
    template_name = 'expense_tracker/week_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_week_expenses = Expense.objects.current_week(self.request.user)

        selected_date = None

        if self.request.method == 'GET' and self.request.GET.get('select_date') is not None:
            selected_date = datetime.strptime(self.request.GET.get('select_date'), '%Y-%m-%d').date()
            current_week_expenses = Expense.objects.filter(
                date__week=selected_date.isocalendar()[1],
                user=self.request.user
                )

        context['categories'], context['weekdays'], context['weekday_total'] = get_weekday_total(
            current_user=self.request.user,
            selected_date=selected_date
            )

        c_def = self.get_user_context(
            expenses=current_week_expenses,
            selected_date=selected_date,
            title='Неделя',
            limit_time='week_limit'
            )

        return dict(list(context.items()) + list(c_def.items()))


class AnnualStatistics(LoginRequiredMixin, StatisticsContextMixin, ListView):
    model = Category
    template_name = 'expense_tracker/annual_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year_expenses = Expense.objects.current_year(self.request.user)

        selected_date = None

        if self.request.method == 'GET' and self.request.GET.get('select_date') is not None:
            selected_date = datetime.strptime(self.request.GET.get('select_date'), '%Y-%m-%d').date()
            current_year_expenses = Expense.objects.filter(
                date__year=selected_date.isocalendar()[0],
                user=self.request.user
                )

        context['categories'], context['months'], context['month_total'] = get_month_total(
            current_user=self.request.user,
            selected_date=selected_date
            )

        c_def = self.get_user_context(
            expenses=current_year_expenses,
            selected_date=selected_date,
            title='Год'
            )

        return dict(list(context.items()) + list(c_def.items()))
