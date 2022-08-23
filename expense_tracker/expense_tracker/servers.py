from django.db.models import Sum, Max, Min, Count
from django.db.models.functions import ExtractIsoWeekDay, ExtractMonth

from expense_tracker.models import Category, Expense, Profile


# statistics

def get_category_calculation(expenses):
    amount_per_category = expenses.values('category') \
        .annotate(total_amount=Sum('amount', default=0.0))
    nonempty_category_pk = amount_per_category.values_list('category', flat=True)

    total = expenses.aggregate(Sum('amount', default=0.0))
    max_amount = expenses.aggregate(Max('amount', default=0.0))
    min_amount = expenses.aggregate(Min('amount', default=0.0))

    return amount_per_category, nonempty_category_pk, total, max_amount, min_amount


def get_weekday_total(current_user):
    categories = Category.objects.filter(user=current_user)

    current_week_expenses = Expense.objects.current_week(current_user)
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


def get_month_total(current_user):
    categories = Category.objects.filter(user=current_user)

    current_year_expenses = Expense.objects.current_year(current_user)

    expenses_by_month = current_year_expenses.values('category') \
        .annotate(month=ExtractMonth('date')).values('category', 'month').annotate(Sum('amount'))

    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    month_total = {}

    for number in range(len(months)):
        month_total[months[number]] = {}
        for category in categories:
            for exp in expenses_by_month:
                if exp['category'] == category.pk:
                    if exp['month'] == number + 1:
                        month_total[months[number]][category.name] = exp['amount__sum']

    return categories, months, month_total


# check limit

def check_limit(limit):
    return limit > 0


def excess_limit(limit, amount):
    if amount > limit:
        return amount - limit
