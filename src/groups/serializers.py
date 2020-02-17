from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import (
    Group, Permission
)
from rest_framework.validators import UniqueValidator

class PermissionSerializer(serializers.ModelSerializer):
      name =serializers.CharField(max_length=255)
      codename =serializers.CharField(max_length=255)
      class Meta:
        model = Permission
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(read_only=True, many=True)
    name = serializers.RegexField(
        regex=r'^(?!.*\ )[A-Za-z\d\-\_]+$',
        required=True,
        validators=[
              UniqueValidator(
                  queryset=Group.objects.all(),
                  message='The groupname is already taken',
              )
        ],
        error_messages={
            'invalid': 'Groupname cannot contain a space or special character',
            'required': 'Groupname is a required property',
        }
    )
    class Meta:
      model = Group
      fields = ('name', 'permissions',)
    
