from rest_framework import serializers
from .models import Bk

class BkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bk
        fields = '__all__'