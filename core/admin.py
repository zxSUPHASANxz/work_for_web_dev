from django.contrib import admin
from .models import Motorbike, Booking

@admin.register(Motorbike)
class MotorbikeAdmin(admin.ModelAdmin):
    list_display = ('id','owner','brand','model','plate_number','year','created_at')
    search_fields = ('brand','model','plate_number')
    list_filter = ('brand',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','user','bike','service_type','booking_date','booking_time','status','created_at')
    list_filter = ('status','service_type')
    search_fields = ('service_type',)
