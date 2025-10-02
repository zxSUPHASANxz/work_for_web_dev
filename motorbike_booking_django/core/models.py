# core/models.py
from django.db import models
from django.conf import settings

class Motorbike(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='motorbikes')
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number or '-'})"

class Booking(models.Model):
    STATUS_CHOICES = [('pending','Pending'),('confirmed','Confirmed'),('done','Done'),('cancelled','Cancelled')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    bike = models.ForeignKey(Motorbike, on_delete=models.CASCADE, related_name='bookings')
    service_type = models.CharField(max_length=100)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Booking #{self.pk} - {self.service_type}"
