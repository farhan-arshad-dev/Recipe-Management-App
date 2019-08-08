"""
Module to define the url for the api application.
"""
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import user_profile, recipe, followers

router = DefaultRouter()
# Use this configration to hide the API root browsable
# router = SimpleRouter()

router.register('profile', user_profile.UserProfilesViewSet)
router.register('login', user_profile.LoginViewSet, base_name='login')
router.register('recipe', recipe.RecipeViewSet)
router.register('follow', followers.FollowingViewSet)

urlpatterns = [
    url('change_password', user_profile.ChangePasswordView.as_view()),
    url('followed_user_recipes', followers.ChangePasswordView.as_view()),
    url(r'', include(router.urls))
]
