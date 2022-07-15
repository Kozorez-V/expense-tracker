from django import template
from expense_tracker.models import *

register = template.Library()


@register.inclusion_tag('expense_tracker/list_expenses.html', takes_context=True)
def expense_history(context):
    request = context['request']
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    return {'expenses': expenses}
