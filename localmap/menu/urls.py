from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.menu_create, name='menu_create'),
    path('list/<uuid:rest_id>', views.menu_list, name='menu_list'),
    path('<uuid:pk>', views.menu_detail, name='menu_detail'),
    path('update/<uuid:pk>', views.menu_update, name='menu_update'),
    path('delete/<uuid:pk>', views.menu_delete, name='menu_delete'),
]