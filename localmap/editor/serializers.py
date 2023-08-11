from rest_framework import serializers
from .models import Editor
from .models import Restaurant
from accounts.serializers import UserInfoSerializer


class EditorSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True) # 유저 정보를 가져온다 !

    class Meta:
        model = Editor
        fields = '__all__'

class EditorSerializer_create(serializers.ModelSerializer):
    rest_id = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), many=True, required=False)

    class Meta:
        model = Editor
        fields = ['user', 'title', 'content', 'rest_id', 'url']

class RestaurantInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('rest_id', 'name','contents','category_name')


class EditorDetailSerializer(serializers.ModelSerializer):
    rest_id = RestaurantInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Editor
        fields = ('ed_no', 'title', 'content', 'rest_id')