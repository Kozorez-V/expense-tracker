from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from ..serializers import UserSerializers
from expense_tracker.models import Category


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializers
    permission_classes = [IsAdminUser | IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(username=self.request.user)

    @action(methods=['get'], detail=True)
    def categories(self, request, pk=None):
        categories = Category.objects.filter(user__pk=pk)
        return Response({'categories': [category.name for category in categories]})