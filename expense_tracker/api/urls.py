from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register(r'category', CategoryViewSet, basename='category')
router.register(r'user', UserViewSet, basename='user')
router.register(r'expense', ExpenseViewSet, basename='expense')
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
