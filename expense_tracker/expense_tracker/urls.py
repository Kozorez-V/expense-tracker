from django.urls import path, include

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('sign_up/', SignUpUser.as_view(), name='sign_up'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('password/', PasswordChangeView.as_view(), name='change_password'),
    path('profile/', profile, name='profile'),
    path('expense_history/', ExpenseHistory.as_view(), name='expense_history'),
    path('categories/', ShowCategories.as_view(), name='categories'),
    path('add_category/', add_category, name='add_category'),
    path('edit_category/<int:pk>', edit_category, name='edit_category'),
    path('delete_category/<int:pk>/', delete_category, name='delete_category'),
    path('transfer_expenses/<int:category_pk>', transfer_expenses, name='transfer_expenses'),
    path('add_expense/', add_expense, name='add_expense'),
    path('edit_expense/<int:pk>', edit_expense, name='edit_expense'),
    path('delete_expense/<int:pk>', delete_expense, name='delete_expense'),
    path('statistics/today/', TodayStatistics.as_view(), name='today_statistics'),
    path('statistics/week/', WeeklyStatistics.as_view(), name='week_statistics'),
    path('statistics/month/', MonthStatistics.as_view(), name='month_statistics'),
    path('statistics/annual/', AnnualStatistics.as_view(), name='annual_statistics'),
    path('__debug__/', include('debug_toolbar.urls'))
]
