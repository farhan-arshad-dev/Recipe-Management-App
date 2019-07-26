"""
Module to define the url for the api application.
"""
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from . import user_profile_views, recipe_views, followers_views

router = DefaultRouter()
# Use this configration to hide the API root browsable
# router = SimpleRouter()

router.register('profile', user_profile_views.UserProfilesViewSet)
router.register('login', user_profile_views.LoginViewSet, base_name='login')
router.register('recipe', recipe_views.RecipeViewSet)
router.register('follow', followers_views.FollowingViewSet)

urlpatterns = [
    url('change_password', user_profile_views.ChangePasswordView.as_view()),
    url(r'', include(router.urls))
]
