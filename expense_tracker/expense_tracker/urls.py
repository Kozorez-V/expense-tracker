from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    # path('register/', RegisterUser.as_view(), name='register')
]