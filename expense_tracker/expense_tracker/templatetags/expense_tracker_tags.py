from django import template
from expense_tracker.models import *

register = template.Library()


@register.inclusion_tag('expense_tracker/list_expenses.html')
def expense_history(sort=None):
    if not sort:
        expenses = Expense.objects.all()
    else:
        expenses = Expense.objects.order_by(sort)

    return {'expenses': expenses}
