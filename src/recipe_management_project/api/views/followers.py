"""
Module contains view that takes a Web request and returns a Web response.
This response can be the HTML contents of a Web page, or a redirect, or a
404 error, or an XML document, or an image or anything.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotAcceptable
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from following_app import models as following_models
from following_app import serializers as following_serializers
from recipe_app.models import RecipeModel
from recipe_app.serializers import RecipeSerializer


class FollowingViewSet(viewsets.ModelViewSet):
    """Handle user create, Retrive, delete the follow othre users"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = following_serializers.UserFollowingSerializer
    queryset = following_models.FollowingModel.objects.all()
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'head', 'delete']

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""

        #  check user try to follow own profile
        following_to = serializer.validated_data['following_to']
        if following_to.id == self.request.user.id:
            raise NotAcceptable("You can't follow your own profile")

        # check user is trying to follow already following user
        is_already_following = following_models.FollowingModel.objects.filter(
            following_to=following_to.id,
            following_by=self.request.user.id
            )
        if is_already_following:
            raise NotAcceptable("You already following {} user".format(
                serializer.validated_data['following_to']))

        serializer.save(following_by=self.request.user)

    def get_queryset(self):
        return following_models.FollowingModel.objects.filter(
            following_by=self.request.user.id)


class ChangePasswordView(ListAPIView):
    """To create an endpoint to get the other followed user recipies"""
    serializer_class = RecipeSerializer
    model = RecipeModel

    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        """This view returns a list of all recipe of followed users"""
        users = list(following_models.FollowingModel.objects.filter(
            following_by=self.request.user.id
            ).values_list("following_to", flat=True))
        return RecipeModel.objects.filter(user_profile__in=users)
