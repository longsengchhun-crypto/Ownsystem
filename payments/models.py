from django.db import models
from bookings.models import Booking

class Payment(models.Model):
    STATUS_CHOICES = (
        ('Pending Verification', 'Pending Verification'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    METHOD_CHOICES = (
        ('ABA Bakong KHQR', 'ABA Bakong KHQR'),
        ('Manual ABA Transfer', 'Manual ABA Transfer'),
    )
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=30, choices=METHOD_CHOICES, default='ABA Bakong KHQR')
    payment_reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    screenshot = models.ImageField(upload_to='screenshots/')
    payment_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending Verification')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ref: {self.payment_reference} - {self.booking.booking_id} ({self.payment_status})"
