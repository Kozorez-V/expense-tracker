from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from ..forms import *


class ShowProfile(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'expense_tracker/profile.html'
