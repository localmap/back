from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from restaurant.serializers import RestSerializer, RestSearchQuerySerializer, RestaurantSerializer, RestDetailSerializer
from .models import Restaurant

from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='post',
    operation_id='식당 등록',
    operation_description='식당을 등록합니다',
    tags=['Restaurant'],
    request_body=RestSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 식당 작성 가능
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def rest_create(request):
    serializer = RestSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        # 인증객체를 통해 인증을 진행하고 사용자 정보를 request.user 객체에 저장
        # 인증정보가 없거나 일치하지않으면 AnonymousUser를 저장
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='get',
    operation_id='식당 리스트 조회',
    operation_description='식당 전체를 조회합니다',
    tags=['Restaurant'],
    responses={200: RestSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])  # 글 확인은 로그인 없이 가능
def rest_list(request):
    rest_list = Restaurant.objects.all().select_related("user","category_name") #쿼리부분
    serializer = RestSerializer(rest_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_id='식당 조회',
    operation_description='식당 1개 조회',
    tags=['Restaurant'],
    responses={200: RestDetailSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def rest_detail(request, pk):
    rest = get_object_or_404(Restaurant.objects.select_related('category_name').prefetch_related('rest_rev__user','rest_rev'), pk=pk)
    serializer = RestDetailSerializer(rest)

    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='put',
    operation_id='식당 수정',
    operation_description='식당을 수정합니다',
    tags=['Restaurant'],
    responses={200: RestSerializer},
    request_body=RestSerializer
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 공지사항 수정 가능
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def rest_update(request, pk):
    rest = get_object_or_404(Restaurant, pk=pk)
    # instance를 지정해줘야 수정될 때 해당 정보가 먼저 들어간 뒤 수정(안정적이다)
    serializer = RestSerializer(instance=rest, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='delete',
    operation_id='식당 삭제',
    operation_description='식당을 삭제합니다',
    tags=['Restaurant'],
    responses={200: RestSerializer}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 공지사항 삭제 가능
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def rest_delete(request, pk):
    rest = get_object_or_404(Restaurant, pk=pk)
    rest.delete()
    return Response(status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_id='식당 검색',
    operation_description='검색어에 해당하는 식당을 조회합니다',
    tags=['Restaurant'],
    query_serializer=RestSearchQuerySerializer,  # 검색어 입력 칸 추가
    responses={200: RestSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def rest_search(request):
    search_keyword = request.GET.get('search', '')

    if search_keyword:
        rest_list = Restaurant.objects.filter(
            Q(name__icontains=search_keyword) | Q(address__icontains=search_keyword)
        ).select_related('area_id', 'category_name', 'user').annotate(
            avg_rating=Avg('rest_rev__rating')).prefetch_related(
            'rest_rev'
        )
    else:
        rest_list = Restaurant.objects.all().select_related('area_id', 'category_name', 'user').annotate(
            avg_rating=Avg('rest_rev__rating')).prefetch_related(
            'rest_rev'
        )

    serializer = RestaurantSerializer(rest_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)