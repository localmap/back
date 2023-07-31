from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.review_create, name='review_create'),
    path('list/<uuid:rest_id>/', views.review_rest, name='review_rest'),
    path('user/<str:user>/', views.review_user, name='review_user'),
    path('delete/<uuid:pk>/', views.review_delete, name='review_delete'),
    path('rest_rate/<uuid:rest_id>/', views.get_avg_rating_rest, name='get_avg_rating_rest'),
    path('user_rate/<str:user>/', views.get_avg_rating_user, name='get_avg_rating_user'),
    path('s3_image_delete/', views.s3_image_delete, name='s3_image_delete'),


]
