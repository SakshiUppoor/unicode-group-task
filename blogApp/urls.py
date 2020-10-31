from django.urls import path, include
from blogApp.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', ObtainAuthTokenView.as_view(), name='login'),
]
