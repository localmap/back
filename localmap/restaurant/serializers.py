from rest_framework import serializers
from .models import Restaurant
from accounts.serializers import UserInfoSerializer


class RestSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True) # 유저 정보를 가져온다 !

    class Meta:
        model = Restaurant
        fields = '__all__'