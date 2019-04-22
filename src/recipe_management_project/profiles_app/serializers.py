from rest_framework import serializers
from . import models

class UserProfileSerializer(serializers.ModelSerializer):
    """A serilizer for our user profile objects."""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password':{'write_only': True}}

    def create(self, validated_data):
        """Create and return a new User."""
        user = models.UserProfile(
            email = validated_data['email'],
            name = validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change endpoint."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for user's Recipes object."""

    class Meta:
        model = models.RecipeModel
        fields = ('id', 'user_profile', 'title', 'brief_description', 'directions', 'ingredients', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}

class UserFollowingSerializer(serializers.ModelSerializer):
    """Serializer for user following item"""

    class Meta:
        model = models.FollowingModel
        fields = ('id', 'following_by', 'following_to', 'created_on')
        extra_kwargs = {'following_by':{'read_only': True}}
    