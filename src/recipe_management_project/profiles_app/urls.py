from django.conf.urls import url
from django.conf.urls import include 

from rest_framework.routers import DefaultRouter

from . import views
router = DefaultRouter()

router.register('profile', views.UserProfilesViewSet)
router.register('login', views.LoginViewSet, base_name='login')
router.register('change_password', views.ChangePasswordView, base_name='change_password')


urlpatterns = [
    url(r'', include(router.urls))
]
