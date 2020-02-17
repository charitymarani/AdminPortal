from django.shortcuts import render
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, ListCreateAPIView)
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import GroupSerializer
from django.contrib.auth.models import Permission,Group
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsAdminUser
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class GroupAPIView(ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = Group.objects.all()
    

    def post(self, request):
        group_data = request.data
        serializer = self.serializer_class(data=group_data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save()
        permission_queryset = []
        try :
          if 'permissions' in group_data.keys():
            permission_data = group_data['permissions']
            if permission_data and len(permission_data) >0:
              for permission in permission_data:
                  perm = Permission.objects.get(pk=permission)
                  permission_queryset.append(perm)
                  group.permissions.add(*permission_queryset)
        except ObjectDoesNotExist:
          return Response({'message': 'Permission not found'})

        response_message = {
            "message": "Group added successfully.",
            "Group_info": serializer.data
        }

        return Response(response_message, status=status.HTTP_201_CREATED)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GroupRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,IsAdminUser,)
    serializer_class = GroupSerializer
    lookup_field = 'id'
    

    def get_group(self, id):
        try:
            return Group.objects.get(id=id)
        except ObjectDoesNotExist:
            raise Http404
    def retrieve(self, request,id):
        group = self.get_group(id)
        serializer = self.serializer_class(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request,id):
        get_group = self.get_group(id)
        group_data = request.data
        serializer = self.serializer_class(get_group, data=group_data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save()
        permission_queryset = []
        try :
          if 'permissions' in group_data.keys():
            permission_data = group_data['permissions']
            if permission_data and len(permission_data) >0:
              for permission in permission_data:
                  perm = Permission.objects.get(pk=permission)
                  permission_queryset.append(perm)
                  group.permissions.add(*permission_queryset)
        except ObjectDoesNotExist:
          return Response({'message': 'Permission not found'})

        response_message = {
            "message": "Group updated successfully.",
            "Group_info": serializer.data
        }

        return Response(response_message, status=status.HTTP_201_CREATED)
    def delete(self, request, id):
        """
        Delete a group
        """
        group= self.get_group(id)
        group.delete()
        return Response({"message": "Group deleted successfully"},status=status.HTTP_204_NO_CONTENT)
