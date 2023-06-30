from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'name')


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email','password')

class UserPwresetSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email',)

class UserPwchangeSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    new_pw = serializers.CharField(write_only=True)
    pw_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('password','new_pw','pw_confirm')
