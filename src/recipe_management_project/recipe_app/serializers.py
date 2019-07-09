"""
Deinfe serializers mechanism for “translating” Django models into other
formats. Usually text-based formats (e.g json)
"""
from rest_framework import serializers
from . import models


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for user's Recipes object."""

    class Meta:
        model = models.RecipeModel
        fields = (
            'id', 'user_profile', 'title', 'brief_description', 'directions',
            'ingredients', 'created_on'
            )
        extra_kwargs = {'user_profile': {'read_only': True}}
