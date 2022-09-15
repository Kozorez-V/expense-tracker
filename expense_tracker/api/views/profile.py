from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..serializers import AdminProfileSerializers, UserProfileSerializers
from expense_tracker.models import Profile


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminProfileSerializers
        return UserProfileSerializers

    def get_queryset(self):
        if self.request.user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(user=self.request.user)