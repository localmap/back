from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.editor_create, name='editor_create'),
    path('list/', views.editor_list, name='editor_list'),
    path('<uuid:pk>', views.editor_detail, name='editor_detail'),
#    path('update/<uuid:pk>', views.editor_update, name='editor_update'),
    path('delete/<uuid:pk>', views.editor_delete, name='editor_delete'),
    path('details/<uuid:pk>', views.editor_details, name='editor_details'),
]
