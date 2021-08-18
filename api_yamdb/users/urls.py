from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_token, send_code

router = DefaultRouter()

router.register('users', UserViewSet, basename='Users')

urlpatterns = [
    path('v1/auth/signup/', send_code, name='register'),
    path('v1/auth/token/', get_token, name='get_token'),
    path('v1/', include(router.urls)),
]
