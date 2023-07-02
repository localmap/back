from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from menu.serializers import MenuSerializer

from .models import Menu
from restaurant.models import Restaurant

from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='post',
    operation_id='메뉴 등록',
    operation_description='메뉴를 등록합니다',
    tags=['Menu'],
    request_body=MenuSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def menu_create(request):
    serializer = MenuSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

@swagger_auto_schema(
    method='get',
    operation_id='해당 레스토랑 메뉴 전체 조회',
    operation_description='해당 레스토랑 메뉴 전체를 조회합니다',
    tags=['Menu'],
    responses={200: MenuSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])  # 메뉴 확인은 로그인 없이 가능
def menu_list(request, rest_id):
    menu_list = Menu.objects.filter(rest_id=rest_id)
    serializer = MenuSerializer(menu_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_id='메뉴 단일 조회',
    operation_description='메뉴 단일 조회',
    tags=['Menu'],
    responses={200: MenuSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def menu_detail(request, pk):
    menu_list = get_object_or_404(Menu, pk=pk)
    serializer = MenuSerializer(menu_list)

    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='put',
    operation_id='메뉴 수정',
    operation_description='메뉴를 수정합니다',
    tags=['Menu'],
    responses={200: MenuSerializer},
    request_body=MenuSerializer
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def menu_update(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    serializer = MenuSerializer(instance=menu, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

@swagger_auto_schema(
    method='delete',
    operation_id='메뉴 삭제',
    operation_description='메뉴를 삭제합니다',
    tags=['Menu'],
    responses={200: MenuSerializer}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def menu_delete(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    menu.delete()
    return Response({'message': '메뉴 삭제 성공'}, status=status.HTTP_200_OK)