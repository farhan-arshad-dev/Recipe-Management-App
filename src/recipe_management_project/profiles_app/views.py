from django.shortcuts import render

from rest_framework import viewsets

from . import models
from . import serializers

# Create your views here.

class UserProfilesViewSet(viewsets.ModelViewSet):
    """handles creating, reading and updating profiles."""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.UpdateOwnProfile,)
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('name', 'email',)