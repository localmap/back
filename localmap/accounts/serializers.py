from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'name','location')

class UserInfoSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_email(self, obj):
        return obj.email

    def get_name(self, obj):
        return obj.name

    class Meta:
        model = get_user_model()
        fields = ('email','name')

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')

    def update(self, instance, validated_data):
        # 비밀번호가 제공된 경우 해시하고 저장
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        return super(UserUpdateSerializer, self).update(instance, validated_data)

class UserPwresetSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email','name')

class UserPwchangeSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    new_pw = serializers.CharField(write_only=True)
    pw_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('password','new_pw','pw_confirm')

class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email','password')