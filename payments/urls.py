from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('upload/<str:booking_id>/', views.payment_upload, name='upload'),
    path('verify/<int:payment_id>/<str:action>/', views.payment_verify, name='verify'),
]
