from django.shortcuts import get_object_or_404
from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from restaurant.serializers import RestSerializer, RestDetailSerializer
from .models import Restaurant
from django.db import connections
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from math import sin, cos, radians, atan2, sqrt
import time
from rest_framework.pagination import LimitOffsetPagination


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
    rest_list = Restaurant.objects.all().select_related("user", "category_name")  # 쿼리부분
    serializer = RestSerializer(rest_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    operation_id='식당 조회',
    operation_description='식당 1개 조회',
    tags=['Restaurant'],
    responses={200: RestDetailSerializer}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def rest_detail(request, pk):
    # 예외 처리를 위해 존재하는지 확인하고 객체를 가져옴
    rest = get_object_or_404(
        Restaurant.objects.select_related("category_name").prefetch_related("rest_rev__user", "rest_rev"),
        pk=pk,
    )

    # 조회수 증가 (view 필드를 F() 표현식으로 업데이트)
    Restaurant.objects.filter(pk=pk).update(view=F("view") + 1)

    # 시리얼라이즈 후 반환
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
    operation_id='근처 이벤트 중인 식당',
    operation_description='근처 5km 이내의 이벤트 중인 식당을 보여줍니다.',
    tags=['Restaurant'],
    manual_parameters=[
        openapi.Parameter(
            name='category',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='카테고리'
        ),
        openapi.Parameter(
            name='sort_by',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='정렬방식'
        ),
        openapi.Parameter(
            name='latitude',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='위도'
        ),
        openapi.Parameter(
            name='longitude',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='경도'
        ),
        openapi.Parameter(
            name='limit',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='한 페이지에 표시될 게시물 갯수'
        ),
        openapi.Parameter(
            name='offset',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='현재 페이지'
        ),
    ],
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_event_rest(request):
    category = request.GET.get('category', None)
    sort_by = request.GET.get('sort_by', 'view')
    latitude = request.GET.get('latitude', None)
    longitude = request.GET.get('longitude', None)

    # Category filtering
    category_filter = f"AND r.category_name = '{category}'" if category else ""

    # Dynamic sorting
    if sort_by.lower() == "rating":
        order_by = "average_rating DESC"
    else:
        order_by = "view DESC"

    nearby_filter = ""
    if latitude and longitude:
        # Distance calculation and filtering for nearby restaurants (within 5km)
        earth_radius = 6371  # Radius of the Earth in km
        nearby_distance = 5  # Distance in km

        query_latitude = float(latitude)
        query_longitude = float(longitude)
        a = f"sin(radians({query_latitude}-r.latitude)/2) * sin(radians({query_latitude}-r.latitude)/2) + cos(radians(r.latitude)) * cos(radians({query_latitude})) * sin(radians({query_longitude}-r.longitude)/2) * sin(radians({query_longitude}-r.longitude)/2)"
        nearby_filter = f"AND ({earth_radius} * 2 * atan2(sqrt({a}), sqrt(1-{a}))) < {nearby_distance}"

    query = f"""
    WITH ranked_review_photos AS (
        SELECT rev.rest_id, pho.url, ROW_NUMBER() OVER (PARTITION BY rev.rest_id ORDER BY rev.created_at DESC) AS rn
        FROM review rev
        LEFT OUTER JOIN photos pho ON rev.review_id = pho.review_id
        WHERE pho.url IS NOT NULL
    )
    SELECT r.category_name, r.rest_id, r.address, r.name, r.latitude, r.longitude, rrp.url AS most_recent_photo_url, ROUND(CAST(AVG(rev.rating) AS NUMERIC), 1) AS average_rating, r.view
    FROM restaurant r
    INNER JOIN events e ON r.rest_id = e.rest_id
    LEFT OUTER JOIN review rev ON r.rest_id = rev.rest_id
    LEFT OUTER JOIN ranked_review_photos rrp ON r.rest_id = rrp.rest_id AND rrp.rn = 1
    WHERE 1=1
    {category_filter}
    {nearby_filter}
    GROUP BY r.rest_id, r.address, r.name, rrp.url, r.view, r.latitude, r.longitude
    ORDER BY {order_by};
    """

    with connections['default'].cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    rest_list = []
    for row in result:
        rest_dict = {
            'category_name': row[0],
            'rest_id': row[1],
            'address': row[2].upper(),
            'name': row[3].upper(),
            'latitude': row[4],
            'longitude': row[5],
            'most_recent_photo_url': row[6],
            'average_rating': row[7],
            'view': row[8],
        }
        rest_list.append(rest_dict)

    # 페이지네이션
    paginator = LimitOffsetPagination()
    limited_results = paginator.paginate_queryset(rest_list, request)
    return paginator.get_paginated_response(limited_results)


@swagger_auto_schema(
    method='get',
    operation_id='근처 식당',
    operation_description='근처 5km 이내의 식당을 보여줍니다.',
    tags=['Restaurant'],
    manual_parameters=[
        openapi.Parameter(
            name='category',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='카테고리'
        ),
        openapi.Parameter(
            name='sort_by',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='정렬방식'
        ),
        openapi.Parameter(
            name='latitude',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='위도'
        ),
        openapi.Parameter(
            name='longitude',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='경도'
        ),
        openapi.Parameter(
            name='limit',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='한 페이지에 표시될 게시물 갯수'
        ),
        openapi.Parameter(
            name='offset',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='현재 페이지'
        ),
    ],
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_near_rest(request):
    category = request.GET.get('category', None)
    sort_by = request.GET.get('sort_by', 'view')
    latitude = request.GET.get('latitude', None)
    longitude = request.GET.get('longitude', None)

    # Category filtering
    category_filter = f"AND r.category_name = '{category}'" if category else ""

    # Dynamic sorting
    if sort_by.lower() == "rating":
        order_by = "average_rating DESC"
    else:
        order_by = "view DESC"

    nearby_filter = ""
    if latitude and longitude:
        # Distance calculation and filtering for nearby restaurants (within 5km)
        earth_radius = 6371  # Radius of the Earth in km
        nearby_distance = 5  # Distance in km

        query_latitude = float(latitude)
        query_longitude = float(longitude)
        a = f"sin(radians({query_latitude}-r.latitude)/2) * sin(radians({query_latitude}-r.latitude)/2) + cos(radians(r.latitude)) * cos(radians({query_latitude})) * sin(radians({query_longitude}-r.longitude)/2) * sin(radians({query_longitude}-r.longitude)/2)"
        nearby_filter = f"AND ({earth_radius} * 2 * atan2(sqrt({a}), sqrt(1-{a}))) < {nearby_distance}"

    query = f"""
    WITH ranked_review_photos AS (
        SELECT rev.rest_id, pho.url, ROW_NUMBER() OVER (PARTITION BY rev.rest_id ORDER BY rev.created_at DESC) AS rn
        FROM review rev
        LEFT OUTER JOIN photos pho ON rev.review_id = pho.review_id
        WHERE pho.url IS NOT NULL
    )
    SELECT r.category_name, r.rest_id, r.address, r.name, r.latitude, r.longitude, rrp.url AS most_recent_photo_url, ROUND(CAST(AVG(rev.rating) AS NUMERIC), 1) AS average_rating, r.view
    FROM restaurant r
    LEFT OUTER JOIN review rev ON r.rest_id = rev.rest_id
    LEFT OUTER JOIN ranked_review_photos rrp ON r.rest_id = rrp.rest_id AND rrp.rn = 1
    WHERE 1=1
    {category_filter}
    {nearby_filter}
    GROUP BY r.rest_id, r.address, r.name, rrp.url, r.view, r.latitude, r.longitude
    ORDER BY {order_by};
    """

    with connections['default'].cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    rest_list = []
    for row in result:
        rest_dict = {
            'category_name': row[0],
            'rest_id': row[1],
            'address': row[2].upper(),
            'name': row[3].upper(),
            'latitude': row[4],
            'longitude': row[5],
            'most_recent_photo_url': row[6],
            'average_rating': row[7],
            'view': row[8],
        }
        rest_list.append(rest_dict)

    paginator = LimitOffsetPagination()
    limited_results = paginator.paginate_queryset(rest_list, request)
    return paginator.get_paginated_response(limited_results)


@swagger_auto_schema(
    method='get',
    operation_id='식당 검색',
    operation_description='식당의 검색결과를 보여줍니다.',
    tags=['Restaurant'],
    manual_parameters=[
        openapi.Parameter(
            name='category',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='카테고리'
        ),
        openapi.Parameter(
            name='sort_by',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='정렬방식'
        ),
        openapi.Parameter(
            name='latitude',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='위도'
        ),
        openapi.Parameter(
            name='longitude',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='경도'
        ),
        openapi.Parameter(
            name='search',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='식당 이름 또는 주소 검색'
        ),
        openapi.Parameter(
            name='limit',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='한 페이지에 표시될 게시물 갯수'
        ),
        openapi.Parameter(
            name='offset',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='현재 페이지'
        ),
    ],
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_search_rest(request):
    category = request.GET.get('category', None)
    sort_by = request.GET.get('sort_by', 'view')
    latitude = request.GET.get('latitude', None)
    longitude = request.GET.get('longitude', None)
    search = request.GET.get('search', None)

    # Category filtering
    category_filter = f"AND r.category_name = '{category}'" if category else ""

    # Dynamic sorting
    if sort_by.lower() == "rating":
        order_by = "average_rating DESC"
    else:
        order_by = "view DESC"

    # Search filtering
    search_filter = ""
    if search:
        search_filter = f"AND (LOWER(r.name) LIKE LOWER('%{search}%') OR LOWER(r.address) LIKE LOWER('%{search}%'))"

    nearby_filter = ""
    if latitude and longitude:
        # Distance calculation and filtering for nearby restaurants (within 5km)
        earth_radius = 6371  # Radius of the Earth in km
        nearby_distance = 5  # Distance in km

        query_latitude = float(latitude)
        query_longitude = float(longitude)
        a = f"sin(radians({query_latitude}-r.latitude)/2) * sin(radians({query_latitude}-r.latitude)/2) + cos(radians(r.latitude)) * cos(radians({query_latitude})) * sin(radians({query_longitude}-r.longitude)/2) * sin(radians({query_longitude}-r.longitude)/2)"
        nearby_filter = f"AND ({earth_radius} * 2 * atan2(sqrt({a}), sqrt(1-{a}))) < {nearby_distance}"

    query = f"""
    WITH ranked_review_photos AS (
        SELECT rev.rest_id, pho.url, ROW_NUMBER() OVER (PARTITION BY rev.rest_id ORDER BY rev.created_at DESC) AS rn
        FROM review rev
        LEFT OUTER JOIN photos pho ON rev.review_id = pho.review_id
        WHERE pho.url IS NOT NULL
    )
    SELECT r.category_name, r.rest_id, r.address, r.name, r.latitude, r.longitude, rrp.url AS most_recent_photo_url, ROUND(CAST(AVG(rev.rating) AS NUMERIC), 1) AS average_rating, r.view
    FROM restaurant r
    LEFT OUTER JOIN review rev ON r.rest_id = rev.rest_id
    LEFT OUTER JOIN ranked_review_photos rrp ON r.rest_id = rrp.rest_id AND rrp.rn = 1
    WHERE 1=1
    {category_filter}
    {nearby_filter}
    {search_filter}
    GROUP BY r.rest_id, r.address, r.name, rrp.url, r.view, r.latitude, r.longitude
    ORDER BY {order_by};
    """

    with connections['default'].cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    rest_list = []
    for row in result:
        rest_dict = {
            'category_name': row[0],
            'rest_id': row[1],
            'address': row[2].upper(),
            'name': row[3].upper(),
            'latitude': row[4],
            'longitude': row[5],
            'most_recent_photo_url': row[6],
            'average_rating': row[7],
            'view': row[8],
        }
        rest_list.append(rest_dict)

    paginator = LimitOffsetPagination()
    limited_results = paginator.paginate_queryset(rest_list, request)
    return paginator.get_paginated_response(limited_results)
