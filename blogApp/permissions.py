from rest_framework import permissions
from blogApp.models import *

class BlogDetails(permissions.BasePermission):
    message = 'You are not allowed to access'

    def has_permission(self, request, view):
        test_email=Blogs.objects.get(pk=view.kwargs['pk']).user
        email=request.user.email
        if str(test_email)==str(email):
            return True
        else:
            return False
