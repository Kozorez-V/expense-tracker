from django.urls import path, include

from .views import *

urlpatterns = [
    path('api/v1/categorylist/', CategoriesAPIView.as_view()),
]
