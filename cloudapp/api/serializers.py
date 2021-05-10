from rest_framework import serializers
from ..models import User, IAMUserAdditional, RootUserAdditional
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from django.shortcuts import render, get_object_or_404
import uuid

def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

class RootUserAuthCustomTokenSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            # Check if user sent email
            if validateEmail(email_or_username):
                user_request = get_object_or_404(
                    User,
                    email=email_or_username,
                )

                email_or_username = user_request.username

            user = authenticate(username=email_or_username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email or username" and "password"')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs




class RootUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # depth = 1
        #extra_fields = ['showAdditional']

#class RootUserAdditionalSerializer(serializers.ModelSerializer):


class RootUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}, 'username': {'read_only': True}}

    def create(self, validated_data):
        username = uuid.uuid4().hex[:30]
        user = User.objects.create_user(**validated_data, username = username)
        return user

class IAMUserAdditionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = IAMUserAdditional
        fields = '__all__'

class IAMUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}, 'username': {'read_only': True}}

    def create(self, validated_data):
        username = uuid.uuid4().hex[:30]
        validated_data['email'] = username + "@xyz.com"
        user = User.objects.create_user(**validated_data, username = username)
        return user

class IAMUserSerializer(serializers.ModelSerializer):
    #root_user = serializers.Integer(source='geofence.id', read_only=True)
    iamuseradditional = IAMUserAdditionalSerializer()   # one to one display of child from parent serializer
    class Meta:
        model = User
        #fields = '__all__'
        #extra_kwargs = {'id': {'read_only': True}, 'username': {'read_only': True}}
        exclude = ('username', 'email', 'password')


# {
#     "password": "",
#     "username": "",
#     "email": "",
#     "name": ""
# }

# {
#     "email_or_username": "priyanshu@gmail.com",
#     "password": "1234"
# }