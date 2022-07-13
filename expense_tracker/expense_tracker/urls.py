from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('sign_up/', SignUpUser.as_view(), name='sign_up'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_expense/', add_expense, name='add_expense'),
    path('settings/', settings, name='settings'),
    path('add_category/', add_category, name='add_category'),
    path('category/<int:pk>/edit/', edit_category, name='edit_category'),
    path('delete_category/<int:pk>/', delete_category, name='delete_category'),
    path('transfer_expenses/<int:category_pk>/transfer/', transfer_expenses, name='transfer_expenses')
]