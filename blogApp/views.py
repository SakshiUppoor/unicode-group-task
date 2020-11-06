from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from blogApp.models import User,Blogs
from blogApp.serializer import UserSerializer,BlogSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.response import Response
from blogApp.serializer import LoginSerializer, RegisterUserSerializer, CommentSerializer, ReplySerializer
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser,FormParser,MultiPartParser,JSONParser
from rest_framework.permissions import IsAuthenticated
from datetime import date
from django.http import Http404
from blogApp.permissions import *

# Create your views here.

class RegisterUser(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = []
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user).key
            data = {
                'response': "User account successfully created",
                'token' : token
            }
        else:
            data = serializer.errors
        return Response(data)

class UserViewSet(#mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()
    permission_classes = []#IsAuthenticated]
    serializer_class = UserSerializer

    def get_authenticators(self):
        # if self.action == 'destroy':
        return super().get_authenticators()
        # return []

    def destroy(self, request, pk=None, **kwargs):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        return UserSerializer

    def get_queryset(self):
        return User.objects.all()


class ObtainAuthTokenView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        context = {}
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        account = authenticate(email=email, password=password)
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            #context['role'] = account.role
            context['token'] = token.key
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid credentials'

        return Response(context)

class BlogPostView(generics.GenericAPIView):
    parser_classes=(FormParser,MultiPartParser,JSONParser)
    permission_classes = (IsAuthenticated,)
    serializer_class=BlogSerializer



    def post(self,request):

        user=User.objects.get(id=request.user.id)
        today=date.today()
        print(today)
        picture=request.data.get("picture")
        caption=request.data.get("caption")
        if caption==None:
            caption=""

        blog=Blogs.objects.create(user=user,
                                created_on=today,
                                last_updated=today,
                                picture=picture,
                                caption=caption,
                                )
        blog.save()
        serializer=BlogSerializer(blog)


        return Response(serializer.data)

    def get(self,request):


        blog=Blogs.objects.filter(user=request.user.id)
        print(blog)

        serializer=BlogSerializer(blog,many=True)

        return Response(serializer.data)


class BlogDetail(generics.GenericAPIView):
    parser_classes=(FormParser,MultiPartParser,JSONParser)
    permission_classes = (IsAuthenticated,BlogDetails,)
    serializer_class=BlogSerializer

    def get_object(self,pk):
        try:
            blog=Blogs.objects.get(pk=pk)
            return blog
        except Blogs.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        
        blog=Blogs.objects.filter(user=request.user.id)
        serializer=BlogSerializer(blog,many=True)
        return Response(serializer.data)

    def put(self,request,pk):
        today=date.today()

        blog=self.get_object(pk)
        picture=request.data.get('picture')
        caption=request.data.get('caption')
        if caption is None:
            caption=blog.caption
        if picture is None:
            picture=blog.picture


        data={
        "user":blog.user.pk,
        "created_on":blog.created_on,
        "last_updated":today,
        "picture":picture,
        "caption":caption
        }
        serializer=BlogSerializer(blog,data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self,request,pk):
        blog=self.get_object(pk)
        blog.delete()
        data={
        "message":"deleted successfully"
        }
        return Response(data)

class UserProfileInfo(generics.GenericAPIView):
    parser_classes=(FormParser,MultiPartParser,JSONParser)
    permission_classes = (IsAuthenticated,)
    serializer_class=BlogSerializer

    def get(self,request):
        user=User.objects.all()
        data=[]
        for i in user:
            lst2=[]
            blog=Blogs.objects.filter(user=i.id)
            for j in blog:
                serializer=BlogSerializer(j)
                lst2.append(serializer.data)

            data3={
            'name':i.first_name +" "+ i.last_name,

            'blogs':lst2
            }
            data.append(data3)
        return Response(data)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (AlwaysTrue(),)
        elif self.request.method == "POST" :
            return (IsAuthenticated(),)
        else:
            return (IsCommentAuthor(),)



class ReplyViewSet(viewsets.ModelViewSet):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (AlwaysTrue(),)
        elif self.request.method == "POST" :
            return (IsAuthenticated(),)
        else:
            return (IsReplyAuthor(),)

            


