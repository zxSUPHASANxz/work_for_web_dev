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

    def clean(self):
        from django.core.exceptions import ValidationError
        import datetime
        if self.year and self.year > datetime.date.today().year:
            raise ValidationError({'year': 'ปีต้องไม่เกินปีปัจจุบัน (Year must not exceed current year)'})

    def __str__(self):
        return f"{self.brand} {self.model} ({self.plate_number or '-'})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('in_progress','In Progress'),
        ('done','Done'),
        ('cancelled','Cancelled')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    bike = models.ForeignKey(Motorbike, on_delete=models.CASCADE, related_name='bookings')
    service_type = models.CharField(max_length=100)
    booking_date = models.DateField(db_index=True)
    booking_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    mechanic = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bookings')
    pickup_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('bike', 'booking_date', 'booking_time')
        indexes = [
            models.Index(fields=['booking_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Booking #{self.pk} - {self.service_type}"
