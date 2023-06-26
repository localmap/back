from django.urls import include, path
from . import views

login_patterns = [
    path('normal/', views.login, name='login'),
]

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', include(login_patterns)),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('pw_change/', views.pw_change, name='pw_change'),
    path('pw_reset/', views.pw_reset, name='pw_reset'),
    path('reset/<str:uidb64>/<str:token>/', views.reset, name='reset'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
]