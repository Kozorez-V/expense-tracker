from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from ..serializers import CategorySerializers, UserSerializers, ExpenseSerializers, ProfileSerializers
from expense_tracker.models import Category, Expense, Profile


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAdminUser | IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            print(self.request.user)
            return User.objects.all()

        return User.objects.filter(username=self.request.user)

    @action(methods=['get'], detail=True)
    def categories(self, request, pk=None):
        categories = Category.objects.filter(user__pk=pk)
        return Response({'categories': [category.name for category in categories]})


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializers
    permission_classes = [IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers
    permission_classes = [IsAuthenticated]
