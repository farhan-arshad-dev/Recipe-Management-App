"""
Deinfe serializers mechanism for “translating” Django models into other
formats. Usually text-based formats (e.g json)
"""
from rest_framework import serializers

from profiles_app.serializers import UserProfileSerializer

from . import models


class UserFollowingSerializer(serializers.ModelSerializer):
    """Serializer for user following item"""

    following_to = UserProfileSerializer()
    class Meta:
        model = models.FollowingModel
        fields = ('id', 'following_to', 'created_on')
