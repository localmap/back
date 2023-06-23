from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.reg_create, name='reg_create'),
    path('list/', views.reg_list, name='reg_list'),
]