from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from ..serializers import UserCategorySerializers, AdminCategorySerializers
from expense_tracker.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['pk', 'user', 'username']
    ordering_fields = ['pk', 'user', 'username']

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminCategorySerializers
        return UserCategorySerializers

    def get_queryset(self):
        if self.request.user.is_staff:
            return Category.objects.all()
        return Category.objects.filter(user=self.request.user)

