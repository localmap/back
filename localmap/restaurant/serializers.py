from rest_framework import serializers
from .models import Restaurant
from review.models import Review
from accounts.serializers import UserInfoSerializer
from review.serializers import ReviewSerializer
from django.db.models import Avg
from urllib.parse import urlparse, urlunparse


class RestSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True) # 유저 정보를 가져온다 !

    class Meta:
        model = Restaurant
        fields = '__all__'

class RestSearchQuerySerializer(serializers.Serializer):
    search = serializers.CharField(required=False, default='', help_text='검색어를 입력하세요 (이름 또는 주소 포함)')

class RestaurantSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField()  # SerializerMethodField를 FloatField로 변경
    url = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ('rest_id', 'address', 'avg_rating', 'name', 'url')

    def get_avg_rating(self, obj):
        reviews = obj.rest_rev.all()
        if reviews:
            return round(reviews.aggregate(Avg('rating'))['rating__avg'], 1)
        else:
            return None

    def get_url(self, obj):
        try:
            review = obj.rest_rev.latest('created_at')  # 최신 리뷰를 가져옴
        except Review.DoesNotExist:  # 리뷰가 없는 경우
            return None

        if review:
            photo = review.photos.first()
            if photo:
                raw_url = photo.url.url
                raw_url = raw_url.replace('https://localmap.s3.amazonaws.com/https%3A/', '')
                parsed_url = urlparse(raw_url)
                cleaned_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
                return cleaned_url

        return None

class RestDetailSerializer(serializers.ModelSerializer):
    rest_rev = ReviewSerializer(many=True, read_only=True) # ReviewSerializer와 연결합니다.
    class Meta:
        model = Restaurant
        fields = ['rest_id', 'area_id', 'category_name',
        'name','address','view','contents','created_at',
        'updated_at','latitude','longitude','introduce','rest_rev',]
