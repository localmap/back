from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.reg_create, name='reg_create'),
    path('list/', views.reg_list, name='reg_list'),
    path('<uuid:pk>', views.reg_detail, name='reg_detail'),
    path('update/<uuid:pk>', views.reg_update, name='reg_update'),
    path('delete/<uuid:pk>', views.reg_delete, name='reg_delete'),
]