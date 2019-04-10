from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, permissions, serializers

# Create your views here.

class UserProfilesViewSet(viewsets.ModelViewSet):
    """handles creating, reading and updating profiles."""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('name', 'email',)

class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token."""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token."""

        return ObtainAuthToken().post(request)


class ChangePasswordView(APIView):
    """An endpoint for changing password."""
    serializer_class = serializers.ChangePasswordSerializer
    model = models.UserProfile

    permission_classes = (permissions.UpdateOwnProfile,)
    authentication_classes = (TokenAuthentication,)

    def patch(self, request, pk=None):
        """Patch request, only updates fields provided in the request"""

        serializer = serializers.ChangePasswordSerializer(data=request.data)
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
    serializer_class = serializers.RecipeSerializer
    queryset = models.RecipeModel.objects.all()
    permission_classes = (permissions.UpdateOwnRecipes, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""
        
        serializer.save(user_profile=self.request.user)

    # override method to get user's own recipe data
    def get_queryset(self):
        return models.RecipeModel.objects.filter(user_profile=self.request.user.id)
