from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from ..models import Category, Expense, Profile
from ..servers import get_amount_per_category, \
    get_nonempty_category_pk, \
    get_min_amount, get_max_amount, \
    get_total_amount, get_weekday_total, \
    get_month_total, get_excess_limit

from datetime import date


class StatisticsContextMixin:
    def get_user_context(self, expenses, limit_time=None, **kwargs):
        context = kwargs

        context['amount_per_category'] = get_amount_per_category(expenses)
        context['nonempty_category_pk'] = get_nonempty_category_pk(expenses)
        context['total_amount'] = get_total_amount(expenses)
        context['max_amount'] = get_max_amount(expenses)
        context['min_amount'] = get_min_amount(expenses)

        if limit_time is not None:
            limit = Profile.objects.get_limit_value(self.request.user, limit_time)

            context['excess_limit'] = get_excess_limit(limit, context['total_amount']['amount__sum'])

        context['title'] = 'Статистика'

        return context


class TodayStatistics(LoginRequiredMixin, StatisticsContextMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'expense_tracker/today_statistics.html'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).only('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = date.today()
        today_expenses = Expense.objects.today(self.request.user)
        c_def = self.get_user_context(expenses=today_expenses, limit_time='day_limit')

        return dict(list(context.items()) + list(c_def.items()))


class WeeklyStatistics(LoginRequiredMixin, StatisticsContextMixin, ListView):
    model = Category
    template_name = 'expense_tracker/week_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'], context['weekdays'], context['weekday_total'] = get_weekday_total(self.request.user)
        current_week_expenses = Expense.objects.current_week(self.request.user)
        c_def = self.get_user_context(expenses=current_week_expenses, limit_time='week_limit')

        return dict(list(context.items()) + list(c_def.items()))


class AnnualStatistics(LoginRequiredMixin, StatisticsContextMixin, ListView):
    model = Category
    template_name = 'expense_tracker/annual_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'], context['months'], context['month_total'] = get_month_total(self.request.user)
        current_year_expenses = Expense.objects.current_year(self.request.user)
        c_def = self.get_user_context(expenses=current_year_expenses)

        return dict(list(context.items()) + list(c_def.items()))