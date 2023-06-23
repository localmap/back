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
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
]