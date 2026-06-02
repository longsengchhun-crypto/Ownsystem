from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('update/<int:project_id>/', views.project_update, name='update'),
    path('upload-file/<int:project_id>/', views.project_upload_file, name='upload_file'),
    path('delete-file/<int:file_id>/', views.project_delete_file, name='delete_file'),
]
