"""
Module contains User recipes views that takes a Web request and
returns a Web response. This response can be the HTML contents of
a Web page, or a redirect, or a 404 error, or an XML document, or
an image or anything.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_app import permissions
from recipe_app import models as recipe_models
from recipe_app import serializers as recipe_serializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating user's recipe items."""

    authentication_classes = (TokenAuthentication,)
    serializer_class = recipe_serializer.RecipeSerializer
    queryset = recipe_models.RecipeModel.objects.all()
    permission_classes = (permissions.UpdateOwnRecipes, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""
        serializer.save(user_profile=self.request.user)

    # override method to get user's own recipe data
    def get_queryset(self):
        return recipe_models.RecipeModel.objects.filter(
            user_profile=self.request.user
            )
