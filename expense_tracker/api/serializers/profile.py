from rest_framework import serializers

from expense_tracker.models import Profile

class ProfileSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profile
        fields = ['user', 'day_limit', 'week_limit', 'month_limit']