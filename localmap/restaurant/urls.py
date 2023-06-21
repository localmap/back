from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.rest_create, name='rest_create'),
    path('list/', views.rest_list, name='rest_list'),
]