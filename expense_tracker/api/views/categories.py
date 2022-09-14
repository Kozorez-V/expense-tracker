from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from ..serializers import UserCategorySerializers, AdminCategorySerializers
from expense_tracker.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminCategorySerializers
        return UserCategorySerializers

    def get_queryset(self):
        if self.request.user.is_staff:
            return Category.objects.all()
        return Category.objects.filter(user=self.request.user)

