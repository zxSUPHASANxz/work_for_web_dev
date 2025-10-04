from django.contrib import admin

from .models import Motorbike, Booking, MechanicProfile
@admin.register(MechanicProfile)
class MechanicProfileAdmin(admin.ModelAdmin):
    list_display = ('user','phone','experience','shop_name','shop_address','created_at')
    search_fields = ('user__username','shop_name','phone')
    list_filter = ('experience',)

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
