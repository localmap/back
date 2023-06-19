from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from hjd.serializers import HjdSerializer, SggSerializer
from django.contrib.gis.db.models.functions import Transform
from django.contrib.gis.geos import Point, Polygon, GEOSGeometry
from hjd.models import Hjd


@swagger_auto_schema(
    method='post',
    operation_id='동네 인증',
    operation_description='gps를 기반으로 동네 정보를 가져옵니다',
    tags=['Hjd'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, description="위도"),
            'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, description="경도"),
            'radius': openapi.Schema(type=openapi.TYPE_NUMBER, description="범위"),
        }
    ),
)
@api_view(['POST'])
@permission_classes([AllowAny])
def hjd_search(request):
    point = Point(request.data.get('longitude'), request.data.get('latitude'), srid=4326)
    point_transformed = point.transform(3857, clone=True)
    buffer = point_transformed.buffer(request.data.get('radius'))
    polygon = GEOSGeometry(buffer, srid=3857)

    hjd_objects = Hjd.objects.filter(geom__intersects=Transform(polygon, 4326))
    serializer = SggSerializer(hjd_objects, many=True)
    return Response(serializer.data)

