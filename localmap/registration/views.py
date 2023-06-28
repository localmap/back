from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from registration.serializers import RegSerializer, ReglistSerializer
from .models import Registration

from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='post',
    operation_id='식당등록 신청',
    operation_description='식당등록을 신청합니다.',
    tags=['Registration'],
    request_body=RegSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])  #유저인 경우
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def reg_create(request):
    serializer = RegSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        # 인증객체를 통해 인증을 진행하고 사용자 정보를 request.user 객체에 저장
        # 인증정보가 없거나 일치하지않으면 AnonymousUser를 저장
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='get',
    operation_id='식당등록 신청 전체 조회',
    operation_description='식당등록 신청을 전체 조회합니다.',
    tags=['Registration'],
    responses={200: ReglistSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])  # 글 확인은 로그인 없이 가능
def reg_list(request):
    reg_list = Registration.objects.all() #쿼리부분
    serializer = ReglistSerializer(reg_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_id='식당등록 신청 단일 조회',
    operation_description='식당등록 신청을 단일 조회합니다.',
    tags=['Registration'],
    responses={200: ReglistSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def reg_detail(request, pk):
    reg = get_object_or_404(Registration, pk=pk)
    serializer = ReglistSerializer(reg)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='put',
    operation_id='식당등록 신청 수정',
    operation_description='식당등록 신청을 수정합니다.',
    tags=['Registration'],
    responses={200: ReglistSerializer}
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def reg_update(request, pk):
    reg = get_object_or_404(Registration, pk=pk)
    serializer = ReglistSerializer(instance=reg, data=request.data)

    if serializer.is_valid(raise_exception=True):
        registration = Registration.objects.get(regist_id=reg.regist_id)
        user_email = registration.user.email

        if user_email == request.user.email :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

@swagger_auto_schema(
    method='delete',
    operation_id='식당등록 신청 삭제',
    operation_description='식당등록 신청을 삭제합니다',
    tags=['Registration'],
    responses={200: ReglistSerializer}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def reg_delete(request, pk):
    reg = get_object_or_404(Registration, pk=pk)
    registration = Registration.objects.get(regist_id=reg.regist_id)
    user_email = registration.user.email

    if user_email == request.user.email:
        reg.delete()
        return Response({'message': '삭제 성공'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)