from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView

from expense_tracker.forms import SignUpForm


def index(request):
    return render(request, 'expense_tracker/index.html', {'title': 'Главная страница'})


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'expense_tracker/sign_up.html'
    success_url = 'login'
