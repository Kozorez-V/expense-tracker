from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('sign_up/', SignUp.as_view(), name='sign_up'),
]