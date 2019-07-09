"""
Module to define the url for the api application.
"""
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
# Use this configration to hide the API root browsable
# router = SimpleRouter()

router.register('profile', views.UserProfilesViewSet)
router.register('login', views.LoginViewSet, base_name='login')
router.register('recipe', views.RecipeViewSet)
router.register('follow', views.FollowingViewSet)

urlpatterns = [
    url('change_password', views.ChangePasswordView.as_view()),
    url(r'', include(router.urls))
]
