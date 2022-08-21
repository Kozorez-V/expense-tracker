from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from ..models import Category, Expense
from ..servers import get_category_calculation, get_weekday_total, get_month_total


class TodayStatistics(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'expense_tracker/today_statistics.html'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).only('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today_expenses = Expense.objects.today(self.request.user)

        context['amount_per_category'], context['nonempty_category_pk'], context['total'], \
        context['max_amount'], context['min_amount'] = get_category_calculation(today_expenses)

        context['title'] = 'Статистика'

        return context


class WeeklyStatistics(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'expense_tracker/week_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_week_expenses = Expense.objects.current_week(self.request.user)

        context['amount_per_category'], context['nonempty_category_pk'], context['total'], \
        context['max_amount'], context['min_amount'] = get_category_calculation(current_week_expenses)

        context['categories'], context['weekdays'], context['weekday_total'] = get_weekday_total(self.request.user)

        context['title'] = 'Статистика'

        return context


class AnnualStatistics(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'expense_tracker/annual_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_year_expenses = Expense.objects.current_year(self.request.user)

        context['amount_per_category'], context['nonempty_category_pk'], context['total'], \
        context['max_amount'], context['min_amount'] = get_category_calculation(current_year_expenses)

        context['categories'], context['months'], context['month_total'] = get_month_total(self.request.user)
        context['title'] = 'Статистика'

        return context
