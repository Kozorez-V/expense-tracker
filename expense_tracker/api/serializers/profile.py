from rest_framework import serializers

from expense_tracker.models import Profile


class AdminProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'day_limit', 'week_limit', 'month_limit']


class UserProfileSerializers(AdminProfileSerializers, serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

   