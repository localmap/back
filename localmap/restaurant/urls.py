from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.rest_create, name='rest_create'),
    path('list/', views.rest_list, name='rest_list'),
    path('<uuid:pk>', views.rest_detail, name='rest_detail'),
    path('update/<uuid:pk>', views.rest_update, name='rest_update'),
    path('delete/<uuid:pk>', views.rest_delete, name='rest_delete'),
]