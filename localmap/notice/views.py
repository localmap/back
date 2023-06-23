from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from notice.serializers import NoticeSerializer
from .models import Notice

from drf_yasg.utils import swagger_auto_schema




@swagger_auto_schema(
    method='post',
    operation_id='공지사항 등록',
    operation_description='공지사항을 등록합니다',
    tags=['Notice'],
    request_body=NoticeSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 공지사항 작성 가능
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def notice_create(request):
    serializer = NoticeSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        # 인증객체를 통해 인증을 진행하고 사용자 정보를 request.user 객체에 저장
        # 인증정보가 없거나 일치하지않으면 AnonymousUser를 저장
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='get',
    operation_id='공지사항 조회',
    operation_description='공지사항 전체를 조회합니다',
    tags=['Notice'],
    responses={200: NoticeSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])  # 글 확인은 로그인 없이 가능
def notice_list(request):
    notice_list = Notice.objects.all() #쿼리부분
    serializer = NoticeSerializer(notice_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_id='공지사항 1개 조회',
    operation_description='공지사항 1개를 조회합니다',
    tags=['Notice'],
    responses={200: NoticeSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])  # 글 확인은 로그인 없이 가능
def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    serializer = NoticeSerializer(notice)

    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='put',
    operation_id='공지사항 수정',
    operation_description='공지사항을 수정합니다',
    tags=['Notice'],
    responses={200: NoticeSerializer}
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 공지사항 수정 가능
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def notice_update(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    # instance를 지정해줘야 수정될 때 해당 정보가 먼저 들어간 뒤 수정(안정적이다)
    serializer = NoticeSerializer(instance=notice, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='delete',
    operation_id='공지사항 삭제',
    operation_description='공지사항을 삭제합니다',
    tags=['Notice'],
    responses={200: NoticeSerializer}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 공지사항 삭제 가능
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    notice.delete()
    return Response(status=status.HTTP_200_OK)