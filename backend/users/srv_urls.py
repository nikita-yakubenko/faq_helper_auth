from django.urls import path
from rest_framework.routers import DefaultRouter

from users.srv_views import get_user_organizations


urlpatterns = [
    path('users/<pk>/organizations/', get_user_organizations, name='user_organizations'),
]
