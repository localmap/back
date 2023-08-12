import uuid, os

from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.http import JsonResponse
from django.db import transaction
from django.conf import settings

from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.throttling import UserRateThrottle

from review.serializers import ReviewSerializer, ReviewCreateSerializer
from .models import Review, Photos

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from aws_module import upload_to_s3, delete_from_s3

class ReviewcreateThrottle(UserRateThrottle):
    rate = '10/day'  # 하루에 최대 10개의 요청


# swagger 데코레이터 설정
file_param = openapi.Parameter('photos', openapi.IN_FORM, description="Select at least one photo file (jpeg/png)",
                               type=openapi.TYPE_ARRAY, items=openapi.Items(type='file', format='binary'),
                               required=False, style='form', explode=False)


@swagger_auto_schema(
    method='post',
    operation_id='리뷰+사진 업로드',
    manual_parameters=[file_param],
    operation_description='리뷰 항목과 사진을 업로드 합니다',
    tags=['Review'],
    responses={200: ReviewCreateSerializer},
    request_body=ReviewCreateSerializer, )
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
@parser_classes([MultiPartParser])
@transaction.atomic()
@throttle_classes([ReviewcreateThrottle])
def review_create(request):
    # import data
    request_data = request.data.dict()
    # import image files
    request_images = request.FILES.getlist('photos')

    review_serializer = ReviewCreateSerializer(data=request_data)

    uploaded_file_names = []
    uploaded_photos = []

    try:
        if review_serializer.is_valid(raise_exception=True):
            review = review_serializer.save(user=request.user)

        if request_images:
            for image in request_images:
                file_name = str(uuid.uuid4()) + os.path.splitext(image.name)[1]
                uploaded_file_names.append(file_name)

                # 사진 URL 저장
                photo = Photos(review=review, url='', user=request.user)
                photo.save()
                uploaded_photos.append(photo)

        for index, image in enumerate(request_images):
            file_name = uploaded_file_names[index]

            # `upload_to_s3()` 함수 호출
            url = upload_to_s3(image, file_name)

            # 업로드된 사진 URL 업데이트
            uploaded_photos[index].url = url
            uploaded_photos[index].save()

        return Response(status=status.HTTP_201_CREATED)

    except Exception as e:
        # 이미 업로드된 파일을 S3에서 삭제합니다.
        if request_images:
            for uploaded_file_name in uploaded_file_names:
                delete_from_s3(settings.AWS_STORAGE_BUCKET_NAME, uploaded_file_name)
        # 예외 처리를 아래에 추가합니다.
        raise exceptions.APIException(str(e))


@swagger_auto_schema(
    method='get',
    operation_id='리뷰 리스트 조회',
    operation_description='해당 식당의 전체 리뷰를 조회합니다',
    tags=['Review'],
    responses={200: ReviewSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])  # 글 확인은 로그인 없이 가능
def review_rest(request, rest_id):
    list_rest = Review.objects.filter(rest_id=rest_id).select_related("user")
    serializer = ReviewSerializer(list_rest, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_id='리뷰 조회',
    operation_description='user별 리뷰 조회',
    tags=['Review'],
    responses={200: ReviewSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def review_user(request, user):
    users = Review.objects.filter(user=user).select_related("user")
    serializer = ReviewSerializer(users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


# @swagger_auto_schema(
#     method='get',
#     operation_id='리뷰 조회',
#     operation_description='user별 리뷰 조회',
#     tags=['Review'],
#     responses={200: ReviewSerializer}
# )
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def review_user(request, user):
#     users = Review.objects.filter(user=user)
#     serializer = ReviewSerializer(users, many=True)
#
#     return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='delete',
    operation_id='리뷰 삭제',
    operation_description='리뷰를 삭제합니다',
    tags=['Review'],
    responses={200: ReviewSerializer}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)

    # 연관된 사진 모든 S3에서 삭제합니다.
    photos = Photos.objects.filter(review=review)
    for photo in photos:
        file_name = str(photo.url).replace("https://localmap.s3.ap-northeast-2.amazonaws.com/images/", "")
        delete_from_s3(settings.AWS_STORAGE_BUCKET_NAME, file_name)

        # 연관된 사진 객체를 삭제합니다.
        photo.delete()

    # 리뷰 객체를 삭제합니다.
    review.delete()

    # 성공적으로 삭제되면 204 No Content를 반환합니다.
    return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method='get',
    operation_id='식당 평점',
    operation_description='식당의 평균 평점을 반환합니다',
    tags=['Review'],
    responses={200: ReviewSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_avg_rating_rest(request, rest_id):
    avg_rating = Review.objects.filter(rest_id=rest_id).aggregate(Avg('rating'))['rating__avg']
    return JsonResponse({"average_rating": avg_rating})


@swagger_auto_schema(
    method='get',
    operation_id='유저 평점',
    operation_description='유저의 평균 평점을 반환합니다',
    tags=['Review'],
    responses={200: ReviewSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_avg_rating_user(request, user):
    avg_rating = Review.objects.filter(user=user).aggregate(Avg('rating'))['rating__avg']
    return JsonResponse({"average_rating": avg_rating})


@swagger_auto_schema(
    method='post',
    operation_id='s3 사진 삭제',
    operation_description='s3 사진을 삭제합니다',
    tags=['Review'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'image_name': openapi.Schema(type=openapi.TYPE_STRING, description="이미지 키값"),
        }
    ),
)
@api_view(['POST'])
@permission_classes([AllowAny])
def s3_image_delete(request):
    image_name = request.data.get('image_name')
    delete_from_s3(settings.AWS_STORAGE_BUCKET_NAME, image_name)
    return Response(status=status.HTTP_200_OK)

