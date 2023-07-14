from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from events.serializers import EventSerializer
from .models import Events

from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='post',
    operation_id='이벤트 등록',
    operation_description='이벤트를 등록합니다',
    tags=['Events'],
    request_body=EventSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])  #유저인 경우
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def event_create(request):
    serializer = EventSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

@swagger_auto_schema(
    method='get',
    operation_id='이벤트 전체 조회',
    operation_description='이벤트 전체를 조회합니다',
    tags=['Events'],
    responses={200: EventSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])  # 이벤트 확인은 로그인 없이 가능
def event_list(request):
    event_list = Events.objects.all() #쿼리부분
    serializer = EventSerializer(event_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_id='이벤트 단일 조회',
    operation_description='이벤트 1개 조회',
    tags=['Events'],
    responses={200: EventSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def event_detail(request, pk):
    event = get_object_or_404(Events, pk=pk)
    serializer = EventSerializer(event)

    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='put',
    operation_id='이벤트 수정',
    operation_description='이벤트를 수정합니다',
    tags=['Events'],
    responses={200: EventSerializer},
    request_body=EventSerializer
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def event_update(request, pk):
    event = get_object_or_404(Events, pk=pk)
    serializer = EventSerializer(instance=event, data=request.data)

    if serializer.is_valid(raise_exception=True) :
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)


@swagger_auto_schema(
    method='delete',
    operation_id='이벤트 삭제',
    operation_description='이벤트를 삭제합니다',
    tags=['Events'],
    responses={200: EventSerializer}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def event_delete(request, pk):
    event = get_object_or_404(Events, pk=pk)
    event.delete()
    return Response({'message': '이벤트 삭제 성공'}, status=status.HTTP_200_OK)