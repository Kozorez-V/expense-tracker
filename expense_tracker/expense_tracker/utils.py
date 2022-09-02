from datetime import date

from django.core.cache import cache

from .models import Profile
from .servers import get_amount_per_category, \
    get_nonempty_category_pk, \
    get_min_amount, get_max_amount, \
    get_total_amount, get_excess_limit


class StatisticsContextMixin:
    def get_user_context(self, expenses, title, limit_time=None, **kwargs):
        context = kwargs

        context['amount_per_category'] = get_amount_per_category(expenses)
        context['nonempty_category_pk'] = get_nonempty_category_pk(expenses)
        context['total_amount'] = get_total_amount(expenses)
        context['max_amount'] = get_max_amount(expenses)
        context['min_amount'] = get_min_amount(expenses)

        if limit_time is not None:
            limit = Profile.objects.get_limit_value(self.request.user, limit_time)

            context['excess_limit'] = get_excess_limit(limit, context['total_amount']['amount__sum'])

        context['date'] = date.today()
        context['title'] = title

        return context