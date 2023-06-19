from django.urls import path
from . import views


urlpatterns = [
    path('search/', views.hjd_search, name='hjd_search'),
]