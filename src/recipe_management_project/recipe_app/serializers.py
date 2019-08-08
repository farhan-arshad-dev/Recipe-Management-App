"""
Deinfe serializers mechanism for “translating” Django models into other
formats. Usually text-based formats (e.g json)
"""
from rest_framework import serializers

from profiles_app.serializers import UserProfileSerializer

from . import models


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for user's Recipes object."""

    class Meta:
        model = models.RecipeModel
        fields = (
            'id', 'created_by', 'title', 'brief_description', 'directions',
            'ingredients', 'created_on'
            )
        extra_kwargs = {'created_by': {'read_only': True}}


class UserRecipeSerializer(RecipeSerializer):
    """Serializer for user's Recipes object."""
    created_by = UserProfileSerializer()
