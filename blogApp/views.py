from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from blogApp.models import User
from blogApp.serializer import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.response import Response
from blogApp.serializer import LoginSerializer, RegisterUserSerializer
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
