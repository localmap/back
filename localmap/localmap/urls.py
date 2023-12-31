from django.contrib import admin
from django.urls import include, path

from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import re_path

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('accounts.urls')),
    path('api/notice/', include('notice.urls')),
    path('api/hjd/', include('hjd.urls')),
    path('api/restaurant/', include('restaurant.urls')),
    path('api/registration/', include('registration.urls')),
    path('api/editor/', include('editor.urls')),
    path('api/event/', include('events.urls')),
    path('api/review/', include('review.urls')),
    path('api/menu/', include('menu.urls')),
    path('api/bks/', include('bks.urls')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
