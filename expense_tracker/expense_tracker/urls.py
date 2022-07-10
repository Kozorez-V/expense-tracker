from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('sign_up/', SignUpUser.as_view(), name='sign_up'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_expense/', add_expense, name='add_expense'),
    path('settings/', settings, name='settings')
]