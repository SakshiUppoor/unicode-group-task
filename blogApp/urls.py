from django.urls import path, include
from blogApp.views import *
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()

router.register('users', UserViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('login/', ObtainAuthTokenView.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('blog_post/',BlogPostView.as_view(),name='blog_post'),
    path('blog_detail/<int:pk>/',BlogDetail.as_view(),name='blog_details'),
    path('user_info/',UserProfileInfo.as_view(),name='user_info'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
