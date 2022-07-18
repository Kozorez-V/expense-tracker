from django import template
from expense_tracker.models import *

from django.core.paginator import Paginator

register = template.Library()


@register.inclusion_tag('expense_tracker/list_expenses.html', takes_context=True)
def expense_history(context):
    request = context['request']
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    paginator = Paginator(expenses, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return {'page_obj': page_obj}
