import os
import jwt
from rest_framework import status, generics
from rest_framework.generics import (
    RetrieveUpdateAPIView, CreateAPIView, ListAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from src import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    PasswordResetSerializer)
from src.settings import SECRET_KEY
from .models import CustomUser


class HomeView(ListAPIView):
    """class to access the home route"""

    def get(self, request):
        return Response("Welcome to fulldeck Authors Haven API")


class RegistrationAPIView(CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_message = {
            "message": "User registered successfully.",
            "user_info": serializer.data
        }

        return Response(response_message, status=status.HTTP_201_CREATED)


class LoginAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)




class PasswordUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def update(self, request, *args, **kwargs):
        token = self.kwargs.get('token')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password != confirm_password:
            return Response({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        password = {
            "password": password
        }
        serializer = self.serializer_class(data=password)
        serializer.is_valid(raise_exception=True)

        try:
            decode_token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = CustomUser.objects.get(email=decode_token['email'])
            user.set_password(request.data.get('password'))
            user.save()
            result = {'message': 'Your password has been reset'}
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)



