from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from token_management import is_token_blacklisted

class TokenBlacklistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 토큰 검증
        jwt_auth = JWTAuthentication()
        header = jwt_auth.get_header(request)
        if header is not None:
            token = jwt_auth.get_raw_token(header)
            if token is not None and is_token_blacklisted(token):
                return JsonResponse({'detail': '토큰이 블랙리스트에 있습니다.'}, status=401)

        response = self.get_response(request)
        return response