from rest_framework import serializers
from .models import Hjd

class HjdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hjd
        fields = '__all__'

class SggSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hjd
        fields = ('adm_nm','id')

