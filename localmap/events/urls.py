from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.event_create, name='event_create'),
    path('list/', views.event_list, name='event_list'),
    path('<uuid:pk>', views.event_detail, name='event_detail'),
    path('update/<uuid:pk>', views.event_update, name='event_update'),
    path('delete/<uuid:pk>', views.event_delete, name='event_delete'),
]