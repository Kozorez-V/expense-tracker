from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..serializers import ProfileSerializers
from expense_tracker.models import Profile


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers
    permission_classes = [IsAuthenticated]