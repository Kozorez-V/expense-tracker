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

        if self.request.method == 'GET' and self.request.GET.get('select_date') is not None:
            expenses = Expense.objects.filter(
                date=self.request.GET.get('select_date'),
                user=self.request.user
                )

        c_def = self.get_user_context(
            expenses=expenses,
            title='День',
            selected_date=self.request.GET.get('select_date'),
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
        c_def = self.get_user_context(
            expenses=month_expenses,
            title='Месяц',
            limit_time='month_limit'
            )

        return dict(list(context.items()) + list(c_def.items()))


class WeeklyStatistics(LoginRequiredMixin, StatisticsContextMixin, ListView):
    model = Category
    template_name = 'expense_tracker/week_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'], context['weekdays'], context['weekday_total'] = get_weekday_total(self.request.user)
        current_week_expenses = Expense.objects.current_week(self.request.user)
        c_def = self.get_user_context(
            expenses=current_week_expenses,
            title='Неделя',
            limit_time='week_limit'
            )

        return dict(list(context.items()) + list(c_def.items()))


class AnnualStatistics(LoginRequiredMixin, StatisticsContextMixin, ListView):
    model = Category
    template_name = 'expense_tracker/annual_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'], context['months'], context['month_total'] = get_month_total(self.request.user)
        current_year_expenses = Expense.objects.current_year(self.request.user)
        c_def = self.get_user_context(
            expenses=current_year_expenses, title='Год'
            )

        return dict(list(context.items()) + list(c_def.items()))
