import random
from django.db import models
from django.conf import settings
from bookings.models import Booking

class Quotation(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='quotation')
    quotation_number = models.CharField(max_length=30, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    estimated_delivery_time = models.CharField(max_length=100, help_text="e.g., 5 business days")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_quotations')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.quotation_number:
            self.quotation_number = f"QT-{random.randint(10000, 99999)}"
            while Quotation.objects.filter(quotation_number=self.quotation_number).exists():
                self.quotation_number = f"QT-{random.randint(10000, 99999)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quotation_number} for {self.booking.booking_id}"
