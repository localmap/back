from rest_framework import serializers
from .models import Review, Photos
from accounts.serializers import UserInfoSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True) # 유저 정보를 가져온다 !

    class Meta:
        model = Review
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = '__all__'

class ReviewCreateSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
