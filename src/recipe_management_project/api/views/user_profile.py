"""
Module contains User profile views that takes a Web request and
returns a Web response. This response can be the HTML contents of
a Web page, or a redirect, or a 404 error, or an XML document, or
an image or anything.
"""
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles_app import models as profile_models
from profiles_app import permissions
from profiles_app import serializers as profile_serializers


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
