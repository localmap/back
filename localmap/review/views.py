from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Avg
from review.serializers import ReviewSerializer, ReviewCreateSerializer
from .models import Review, Photos
from drf_yasg.utils import swagger_auto_schema
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser
from drf_yasg import openapi
import boto3, uuid, os, mimetypes

s3 = boto3.client('s3', region_name='ap-northeast-2',
                  aws_access_key_id='AKIATQLW6UN72MQCLJUY',
                  aws_secret_access_key='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')


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
def review_create(request):
    #import data
    request_data = request.data.dict()
    #import image files
    request_images = request.FILES.getlist('photos')

    review_serializer = ReviewCreateSerializer(data=request_data)

    if review_serializer.is_valid(raise_exception=True):
        review = review_serializer.save(user=request.user)

    if request_images:
        for image in request_images:
            file_name = str(uuid.uuid4()) + os.path.splitext(image.name)[1]  # 파일명에 확장자 추가
            object_key = f'images/{file_name}'

            # 이미지 파일의 MIME 유형 찾기
            content_type, _ = mimetypes.guess_type(file_name)

            # S3에 이미지 업로드
            s3.upload_fileobj(image, 'localmap', object_key,
                              ExtraArgs={'ACL': 'public-read', 'ContentDisposition': 'inline',
                                         'ContentType': content_type})

            # 사진 URL 생성
            url = f"https://localmap.s3.ap-northeast-2.amazonaws.com/{object_key}"

            # 사진 URL 저장
            photo = Photos(review=review, url=url)
            photo.save()

    return Response(status=status.HTTP_201_CREATED)


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
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def review_delete(request, pk):
    rest = get_object_or_404(Review, pk=pk)
    rest.delete()
    return Response(status=status.HTTP_200_OK)


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



