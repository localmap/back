from drf_yasg import openapi
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import update_last_login
from accounts.serializers import UserSerializer
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from accounts.token import account_activation_token
from accounts.text import message
from django.shortcuts import redirect
from accounts.models import User

@swagger_auto_schema(
    method='post',
    operation_id='일반 회원가입',
    operation_description='회원가입을 진행합니다.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description="비밀번호"),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="이름"),
        }
    ),
    tags=['유저'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="Access Token"),
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token"),
            }
        )
    )}
)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    email = request.data.get('email')
    password = request.data.get('password')
    name = request.data.get('name')

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.save(email=email, name=name)  # 필드 값 바로 저장

        user.set_password(password)
        user.save()

        # Email activation
        try:
            validate_email(email) # 이메일 주소를 유효성 검사

            current_site = get_current_site(request) #현재 사이트를 가져옴
            domain = current_site.domain #현재 사이트의 도메인을 추출
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk)) #사용자의 기본 키를 base64로 인코딩
            token = account_activation_token.make_token(user) #사용자를 위한 인증 토큰을 생성
            message_data = message(domain, uidb64, token) #도메인, uidb64 및 토큰을 사용하여 이메일 메시지 내용을 생성

            mail_title = "이메일 인증을 완료해주세요" #이메일의 제목 설정
            mail_to = request.data.get('email') #요청 데이터에서 수신자 이메일 주소를 가져옴
            email = EmailMessage(mail_title, message_data, to=[mail_to]) # 제목, 내용 및 수신자로 이메일 메시지 객체를 생성
            email.send() #이메일 전송

            return Response({'message': 'SUCCESS'}, status=status.HTTP_201_CREATED)

        except ValidationError:
            return Response({'message': '유효한 이메일 주소를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()
    if user is not None and user.check_password(password):
        # 추가적인 조건 검사 (예: 이메일 인증 여부)
        if user.is_active:
            # 인증에 성공하고 추가적인 조건도 충족한 경우
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)

            return Response({'refresh_token': str(refresh),
                             'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            # 인증에는 성공했지만 추가적인 조건을 충족하지 않은 경우 (예: 이메일 미인증)
            return Response({'message': '이메일 인증을 하세요.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        # 인증에 실패한 경우알림
        return Response({'message': '아이디 또는 비밀번호가 일치하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([AllowAny])
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            return redirect('http://127.0.0.1:8000/swagger/')
        else:
            return Response({"message": "인증 실패"}, status=status.HTTP_401_UNAUTHORIZED)

    except ValidationError:
        return Response({"message": "유효성 검사 오류"}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({"message": "잘못된 키"}, status=status.HTTP_400_BAD_REQUEST)