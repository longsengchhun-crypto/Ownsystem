from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('reports/export-excel/', views.export_excel_report, name='export_excel'),
    path('reports/export-pdf/', views.export_pdf_report, name='export_pdf'),
]
