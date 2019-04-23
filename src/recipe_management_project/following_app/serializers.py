from rest_framework import serializers
from . import models

class UserFollowingSerializer(serializers.ModelSerializer):
    """Serializer for user following item"""

    class Meta:
        model = models.FollowingModel
        fields = ('id', 'following_by', 'following_to', 'created_on')
        extra_kwargs = {'following_by':{'read_only': True}}