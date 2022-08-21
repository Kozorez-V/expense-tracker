from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from ..forms import *


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'expense_tracker/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context


def logout_user(request):
    logout(request)
    return redirect('login')
