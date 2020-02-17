import os
import jwt
from rest_framework import status, generics
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, CreateAPIView)
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
from .models import RegularUser, CustomUser
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import PermissionRequiredMixin
from ..permissions import IsAdminUser
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


class HomeView(ListAPIView):
    """class to access the home route"""

    def get(self, request):
        return Response("Welcome to Adrian admin portal")


class UserAPIView(CreateAPIView):
    # Allow user with add_regular user permission to hit this endpoint.
    permission_classes = (IsAuthenticated, IsAdminUser)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer
    queryset = CustomUser.objects.all()

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        saved_user = serializer.save()
        group_queryset = []
        try:
            if 'groups' in user.keys():
                group_data = user['groups']
                if len(group_data) > 0:
                    for group in group_data:
                        grp = Group.objects.get(pk=group)
                        group_queryset.append(grp)
                        saved_user.groups.add(*group_queryset)
        except ObjectDoesNotExist:
            return Response({'message': 'Group not found'})
        response_message = {
            "message": "User added successfully.",
            "user_info": serializer.data
        }
        return Response(response_message, status=status.HTTP_201_CREATED)

    

class ListUsersView(ListAPIView):
    """class to list users"""
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = RegistrationSerializer
    queryset = CustomUser.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class RegistrationAPIView(CreateAPIView):
    # Allow any user to hit this endpoint.
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


class UserRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get_user(self, id):
        try:
            return CustomUser.objects.get(id=id)
        except ObjectDoesNotExist:
            raise Http404

    def retrieve(self, request, id):
        user = self.get_user(id)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, id):
        user = self.get_user(id)
        serializer_data = request.data
        serializer = self.serializer_class(
            user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        saved_user = serializer.save()
        group_queryset = []
        try:
            if 'groups' in serializer_data.keys():
                group_data = serializer_data['groups']
                if len(group_data) > 0:
                    for group in group_data:
                        grp = Group.objects.get(pk=group)
                        group_queryset.append(grp)
                        saved_user.groups.add(*group_queryset)
        except ObjectDoesNotExist:
            return Response({'message': 'User not found'})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        user = self.get_user(id)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


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
