from rest_framework import serializers
from .models import Review
from accounts.serializers import UserInfoSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True) # 유저 정보를 가져온다 !

    class Meta:
        model = Review
        fields = '__all__'