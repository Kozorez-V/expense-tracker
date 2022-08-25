from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from ..models import Category, Expense, Profile
from ..servers import get_amount_per_category, \
    get_nonempty_category_pk, \
    get_min_amount, get_max_amount, \
    get_total_amount, get_weekday_total, \
    get_month_total, check_limit, get_excess_limit

from datetime import date


class TodayStatistics(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'expense_tracker/today_statistics.html'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).only('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today_expenses = Expense.objects.today(self.request.user)

        limit = Profile.objects.get_limit_value(self.request.user, 'day_limit')

        context['amount_per_category'] = get_amount_per_category(today_expenses)
        context['nonempty_category_pk'] = get_nonempty_category_pk(today_expenses)
        context['total_amount'] = get_total_amount(today_expenses)
        context['max_amount'] = get_max_amount(today_expenses)
        context['min_amount'] = get_min_amount(today_expenses)

        if get_excess_limit(limit, get_total_amount(today_expenses)['amount__sum']):
            context['excess_limit'] = get_excess_limit(limit, get_total_amount(today_expenses)['amount__sum'])

        context['date'] = date.today()
        context['title'] = 'Статистика'

        return context


class WeeklyStatistics(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'expense_tracker/week_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_week_expenses = Expense.objects.current_week(self.request.user)

        context['amount_per_category'] = get_amount_per_category(current_week_expenses)
        context['nonempty_category_pk'] = get_nonempty_category_pk(current_week_expenses)
        context['total_amount'] = get_total_amount(current_week_expenses)
        context['max_amount'] = get_max_amount(current_week_expenses)
        context['min_amount'] = get_min_amount(current_week_expenses)

        context['categories'], context['weekdays'], context['weekday_total'] = get_weekday_total(self.request.user)

        context['title'] = 'Статистика'

        return context


class AnnualStatistics(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'expense_tracker/annual_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_year_expenses = Expense.objects.current_year(self.request.user)

        context['amount_per_category'] = get_amount_per_category(current_year_expenses)
        context['nonempty_category_pk'] = get_nonempty_category_pk(current_year_expenses)
        context['total_amount'] = get_total_amount(current_year_expenses)
        context['max_amount'] = get_max_amount(current_year_expenses)
        context['min_amount'] = get_min_amount(current_year_expenses)

        context['categories'], context['months'], context['month_total'] = get_month_total(self.request.user)
        context['title'] = 'Статистика'

        return context
