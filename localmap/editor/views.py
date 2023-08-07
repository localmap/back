import os, uuid

from django.shortcuts import get_object_or_404
from django.db import connection, transaction
from django.http import JsonResponse
from django.conf import settings

from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser

from restaurant.models import Restaurant
from editor.serializers import EditorSerializer, EditorSerializer_create, EditorDetailSerializer
from .models import Editor

from drf_yasg.utils import swagger_auto_schema

from aws_module import upload_to_s3, delete_from_s3

@swagger_auto_schema(
    method='post',
    operation_id='컬럼 등록',
    operation_description='컬럼을 등록합니다',
    tags=['Editor'],
    request_body=EditorSerializer_create,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 식당 작성 가능
@authentication_classes([JWTAuthentication]) # JWT 토큰 확인
@parser_classes([MultiPartParser])
@transaction.atomic()
def editor_create(request):
    restaurants = request.data.pop('rest_id', [])
    request_data = request.data.dict()
    request_image = request.FILES.get('image')

    serializer = EditorSerializer_create(data=request_data)
    try:
        if serializer.is_valid(raise_exception=True):
            editor_obj = serializer.save(user=request.user)

    # 식당 객체를 추가하고 저장
        for restaurant_id in restaurants:
            restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
            editor_obj.rest_id.add(restaurant)

        if request_image:
            file_name = str(uuid.uuid4()) + os.path.splitext(request_image.name)[1]

        # aws_module을 이용하여 S3에 사진 업로드
            s3_image_url = upload_to_s3(request_image, file_name)

        # 반환된 URL을 editor_obj에 저장
            editor_obj.image_url = s3_image_url

            editor_obj.save()
        return Response(status=status.HTTP_201_CREATED)
    except Exception as e:
        # 이미 업로드된 파일을 S3에서 삭제합니다.
        if request_image:
            delete_from_s3(settings.AWS_STORAGE_BUCKET_NAME, s3_image_url)
        # 예외 처리를 아래에 추가합니다.
        raise exceptions.APIException(str(e))


@swagger_auto_schema(
    method='get',
    operation_id='컬럼 리스트 조회',
    operation_description='컬럼 전체를 조회합니다',
    tags=['Editor'],
    responses={200: EditorSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])  # 글 확인은 로그인 없이 가능
def editor_list(request):
    rest_list = Editor.objects.all().select_related('user').prefetch_related('rest_id')  # 쿼리부분
    serializer = EditorSerializer(rest_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_id='컬럼 조회',
    operation_description='컬럼 1개 조회',
    tags=['Editor'],
    responses={200: EditorSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def editor_detail(request, pk):
    rest = get_object_or_404(Editor, pk=pk)
    serializer = EditorSerializer(rest)

    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='put',
    operation_id='컬럼 수정',
    operation_description='컬럼을 수정합니다',
    tags=['Editor'],
    responses={200: EditorSerializer},
    request_body=EditorSerializer
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 공지사항 수정 가능
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def editor_update(request, pk):
    rest = get_object_or_404(Editor, pk=pk)
    # instance를 지정해줘야 수정될 때 해당 정보가 먼저 들어간 뒤 수정(안정적이다)
    serializer = EditorSerializer(instance=rest, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='delete',
    operation_id='컬럼 삭제',
    operation_description='컬럼을 삭제합니다',
    tags=['Editor'],
    responses={200: EditorSerializer}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 공지사항 삭제 가능
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def editor_delete(request, pk):
    rest = get_object_or_404(Editor, pk=pk)
    rest.delete()
    return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_id='컬럼 페이지',
    operation_description='페이지 요청값',
    tags=['Editor'],
)
@api_view(['GET'])
@permission_classes([AllowAny])
def editor_details(request, pk):
    query = """
        SELECT
            "editor"."ed_no",
            "editor"."title",
            "editor"."content",
            "restaurant"."rest_id",
            "restaurant"."category_name",
            "restaurant"."name",
            "restaurant"."contents"
        FROM
            "editor"
        LEFT OUTER JOIN
            "editor_rest_id" ON ("editor"."ed_no" = "editor_rest_id"."editor_id")
        LEFT OUTER JOIN
            "restaurant" ON ("editor_rest_id"."restaurant_id" = "restaurant"."rest_id")
        WHERE
            "editor"."ed_no" = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [pk])
        result = cursor.fetchall()

    editor_dict = {}
    restaurants_list = []
    for row in result:
        if not editor_dict:
            editor_dict = {
                'ed_no': row[0],
                'title': row[1],
                'content': row[2],
            }
        if row[4]:
            restaurant_dict = {
                'rest_id': row[3],
                'category_name': row[4],
                'name': row[5],
                'contents': row[6],
            }
            restaurants_list.append(restaurant_dict)
    editor_dict['rest_id'] = restaurants_list
    return JsonResponse(editor_dict, status=200)


"""
def editor_details(request, pk):
    editor = get_object_or_404(Editor, pk=pk)
    serializer = EditorDetailSerializer(editor)

    return Response(serializer.data, status=status.HTTP_200_OK)
"""
