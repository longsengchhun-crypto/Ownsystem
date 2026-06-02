import random
from django.db import models
from django.conf import settings
from services.models import Service

class Booking(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Quoted', 'Quoted'),
        ('Awaiting Payment', 'Awaiting Payment'),
        ('Paid', 'Paid'),
        ('In Progress', 'In Progress'),
        ('Revision Requested', 'Revision Requested'),
        ('Completed', 'Completed'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    
    booking_id = models.CharField(max_length=30, unique=True, primary_key=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='bookings')
    project_title = models.CharField(max_length=200)
    project_description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    requirement_file = models.FileField(upload_to='requirements/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.booking_id:
            # Generate a nice premium-style booking ID e.g. BK-78392
            self.booking_id = f"BK-{random.randint(10000, 99999)}"
            while Booking.objects.filter(booking_id=self.booking_id).exists():
                self.booking_id = f"BK-{random.randint(10000, 99999)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.project_title}"
