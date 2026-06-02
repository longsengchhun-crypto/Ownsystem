from django.urls import path
from . import views

app_name = 'quotations'

urlpatterns = [
    path('create/<str:booking_id>/', views.quotation_create, name='create'),
    path('accept/<str:quotation_number>/', views.quotation_accept, name='accept'),
]
