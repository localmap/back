from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Bk
from .serializers import BkSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='POST',
    operation_id='북마크 등록 및 삭제',
    operation_description='북마크를 등록하거나 삭제합니다.',
    tags=['Bk'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'rest_id': openapi.Schema(type=openapi.TYPE_STRING),
            'toggle_value': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        },
        required=['rest_id', 'toggle_value'],
    )
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bk_toggle(request):
    rest_id = request.data.get('rest_id')
    toggle_value = request.data.get('toggle_value')

    try:
        bk = Bk.objects.get(user=request.user)

        if toggle_value:
            bk.rest_id.add(rest_id)  # rest_id 추가
        else:
            bk.rest_id.remove(rest_id)  # rest_id 삭제

    except Bk.DoesNotExist:
        bk = Bk.objects.create(user=request.user)
        bk.rest_id.add(rest_id)  # rest_id 추가

    serializer = BkSerializer(bk)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='GET',
    operation_id='북마크 전체 리스트',
    operation_description='북마크 전체 리스트입니다.',
    tags=['Bk'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bk_list(request):
    try:
        bookmarks = Bk.objects.filter(user=request.user)
        serializer = BkSerializer(bookmarks, many=True)
        return Response(serializer.data)
    except Bk.DoesNotExist:
        return Response({'message': '북마크가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(
    method='GET',
    operation_id='북마크 갯수 확인',
    operation_description='해당 유저의 북마크 개수를 확인합니다.',
    tags=['Bk'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bk_count(request):
    try:
        bk = Bk.objects.get(user=request.user)
        bk_count = bk.rest_id.count()
    except Bk.DoesNotExist:
        bk_count = 0
    return Response({"bk_count": bk_count})

@swagger_auto_schema(
    method='get',
    operation_id='레스토랑 북마크 수 확인',
    operation_description='해당 레스토랑의 북마크를 한 유저 수를 확인합니다.',
    tags=['Bk'],
    manual_parameters=[
        openapi.Parameter(
            name='rest_id',
            in_=openapi.IN_QUERY,
            description='레스토랑 ID (UUID)',
            type=openapi.TYPE_STRING
        )
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def rest_bk_count(request):
    try :
        rest_id = request.GET.get('rest_id')
        bk_count = Bk.objects.filter(rest_id=rest_id).count()
    except Bk.DoesNotExist:
        bk_count = 0
    return Response({'bk_count': bk_count}, status=status.HTTP_200_OK)