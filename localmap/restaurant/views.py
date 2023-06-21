from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from restaurant.serializers import RestSerializer
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
    operation_id='식당 조회',
    operation_description='식당 전체를 조회합니다',
    tags=['Restaurant'],
    responses={200: RestSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])  # 글 확인은 로그인 없이 가능
def rest_list(request):
    rest_list = Restaurant.objects.all() #쿼리부분
    serializer = RestSerializer(rest_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)