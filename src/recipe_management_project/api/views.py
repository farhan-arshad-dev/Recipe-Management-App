from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from following_app import models as following_models
from following_app import serializers as following_serializers
from profiles_app import models as profile_models
from profiles_app import permissions
from profiles_app import serializers as profile_serializers
from recipe_app import models as recipe_models
from recipe_app import serializers as recipe_serializer

# Create your views here.


class UserProfilesViewSet(viewsets.ModelViewSet):
    """handles creating, reading and updating profiles."""

    serializer_class = profile_serializers.UserProfileSerializer
    queryset = profile_models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    # Disable put method
    http_method_names = ['get', 'post', 'head', 'patch']


class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token."""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token."""

        return ObtainAuthToken().post(request)


class ChangePasswordView(APIView):
    """An endpoint for changing password."""
    serializer_class = profile_serializers.ChangePasswordSerializer
    model = profile_models.UserProfile

    permission_classes = (permissions.UpdateOwnProfile,)
    authentication_classes = (TokenAuthentication,)

    def patch(self, request, pk=None):
        """Patch request, only updates fields provided in the request"""

        serializer = profile_serializers.ChangePasswordSerializer(
            data=request.data
            )
        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not request.user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            request.user.set_password(serializer.data.get("new_password"))
            request.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        users = list(following_models.FollowingModel.objects.filter(
            following_by=self.request.user.id
            ).values_list("following_to", flat=True))
        users.append(self.request.user.id)
        return recipe_models.RecipeModel.objects.filter(user_profile__in=users)


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
        if(following_to.id == self.request.user.id):
            raise NotAcceptable("You can't follow your own profile")

        # check user is trying to follow already following user
        is_already_following = following_models.FollowingModel.objects.\
            filter(
                following_to=following_to.id,
                following_by=self.request.user.id
                )
        if(is_already_following):
            raise NotAcceptable("You already following {} user".format(
                serializer.validated_data['following_to']))

        serializer.save(following_by=self.request.user)

    def get_queryset(self):
        return following_models.FollowingModel.objects.\
            filter(following_by=self.request.user.id)
