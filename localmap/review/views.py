from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from review.serializers import ReviewSerializer
from .models import Review
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Avg
from django.http import JsonResponse

@swagger_auto_schema(
    method='post',
    operation_id='리뷰 등록',
    operation_description='리뷰를 등록합니다',
    tags=['Review'],
    request_body=ReviewSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def review_create(request):
    serializer = ReviewSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        # 인증객체를 통해 인증을 진행하고 사용자 정보를 request.user 객체에 저장
        # 인증정보가 없거나 일치하지않으면 AnonymousUser를 저장
        serializer.save(user=request.user)
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
    list_rest = Review.objects.filter(rest_id=rest_id)
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
    users = Review.objects.filter(user=user)
    serializer = ReviewSerializer(users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


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