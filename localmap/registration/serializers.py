from rest_framework import serializers
from .models import Registration
from accounts.serializers import UserInfoSerializer


class RegSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True) # 유저 정보를 가져온다 !

    class Meta:
        model = Registration
        fields = '__all__'

class ReglistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ('regist_id', 'name', 'address','latitude', 'longitude', 'category_name')