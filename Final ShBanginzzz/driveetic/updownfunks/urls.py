from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'), 
    path('cdashboard/', views.dashboard_view, name='cdashboard'),
    path('file/upload/', views.file_upload_view, name='file_upload'),
    path('file/upload/<int:pk>/', views.file_upload_view, name='file_upload'),
    path('file/<pk>/download/', views.file_download_view, name='file_download'),
    path('file/<pk>/delete/', views.file_delete_view, name='file_delete'),
    
    path('create_folder/', views.create_folder_view, name='create_folder'),
    path('folders/<int:pk>/', views.folder_detail_view, name='folder_detail'),
    path('folders/<pk>/delete/', views.delete_folder_view, name='delete_folder'),
    path('folders/int:<pk>/upload/', views.upload_folder_view, name='upload_folder'),
    path('download_folder/<int:folder_pk>/', views.download_folder_view, name='download_folder'),
    path('move_file/<int:file_pk>/', views.move_file, name='move_file'),

]