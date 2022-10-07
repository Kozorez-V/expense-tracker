from django.db.models import Sum, Max, Min
from django.db.models.functions import ExtractIsoWeekDay, ExtractMonth

from .models import Category, Expense


# statistics

def get_amount_per_category(expenses):
    return expenses.values('category') \
        .annotate(total_amount=Sum('amount', default=0.0))


def get_nonempty_category_pk(amount_per_category):
    return amount_per_category.values_list('category', flat=True)


def get_total_amount(expenses):
    return expenses.aggregate(Sum('amount', default=0.0))


def get_max_amount(expenses):
    return expenses.aggregate(Max('amount', default=0.0))


def get_min_amount(expenses):
    return expenses.aggregate(Min('amount', default=0.0))


def get_date(request):
    if request.method == 'GET':
        print(request.GET)


# weekly
def get_weekday_total(current_user):
    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    weekday_total = {}
    categories = Category.objects.get_user_categories(current_user)

    current_week_expenses = Expense.objects.current_week(current_user)
    expenses_by_weekday = current_week_expenses.values('category', 'date') \
        .annotate(weekday=ExtractIsoWeekDay('date')).annotate(Sum('amount'))

    for number in range(len(weekdays)):
        weekday_total[weekdays[number]] = {}
        for category in categories:
            for exp in expenses_by_weekday:
                if exp['category'] == category.pk:
                    if exp['weekday'] == number + 1:
                        weekday_total[weekdays[number]][category.name] = exp['amount__sum']

    return categories, weekdays, weekday_total


# monthly
def get_month_total(current_user):
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    month_total = {}
    categories = Category.objects.get_user_categories(current_user)

    current_year_expenses = Expense.objects.current_year(current_user)
    expenses_by_month = current_year_expenses.values('category') \
        .annotate(month=ExtractMonth('date')).values('category', 'month').annotate(Sum('amount'))

    for number in range(len(months)):
        month_total[months[number]] = {}
        for category in categories:
            for exp in expenses_by_month:
                if exp['category'] == category.pk:
                    if exp['month'] == number + 1:
                        month_total[months[number]][category.name] = exp['amount__sum']

    return categories, months, month_total


# limit
def check_limit(limit):
    return limit > 0


def get_excess_limit(limit, total_amount):
    if check_limit(limit):
        if total_amount <= limit:
            return 0

        return total_amount - limit
