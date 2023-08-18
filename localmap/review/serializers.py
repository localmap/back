from rest_framework import serializers
from .models import Review, Photos
from accounts.serializers import UserInfoSerializer

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = '__all__'

class PhotoReadSerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField(source='file_url')
    class Meta:
        model = Photos
        fields = ['url']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True) # 유저 정보를 가져온다 !
    photos = PhotoReadSerializer(many=True, read_only=True)
    class Meta:
        model = Review
        fields = '__all__'

class ReviewCreateSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
