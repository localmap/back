from rest_framework import serializers
from .models import Events


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Events
        fields = '__all__'

class EventSerializer_create(serializers.ModelSerializer):

    class Meta:
        model = Events
        fields = ['rest_id','name','amount','content','url']