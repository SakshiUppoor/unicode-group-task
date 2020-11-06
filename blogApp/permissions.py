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

class IsCommentAuthor(permissions.BasePermission):
    message = "Only Comment author can update the comment"
    
    def has_object_permission(self,request,view,obj):
        if User.objects.filter(email=request.user).exists():
            user = User.objects.get(email=request.user)
            return obj.comment_by == user
        else:
            return False

class IsReplyAuthor(permissions.BasePermission):
    message = "Only Reply author can update the reply"

    def has_object_permission(self,request,view,obj):
        if User.objects.filter(email=request.user).exists():
            user = User.objects.get(email=request.user)
            return obj.reply_by == user
        else:
            return False

class AlwaysTrue(permissions.BasePermission):
    def has_permission(self, request, view):
        return True