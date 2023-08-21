from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets, generics, status
from django.contrib.auth import authenticate, login
from rest_framework.response import Response

# from core.serializers import UserRegistrationSerializer, UserSerializer
from rest_framework.authtoken.models import Token

from authenticate.serializers import UserRegistrationSerializer, UserSerializer

User = get_user_model()


# Create your views here.


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class UserLoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
