
# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.models import User
from .models import Motorbike, Booking

class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class MotorbikeForm(forms.ModelForm):
    class Meta:
        model = Motorbike
        fields = ('brand','model','plate_number','year')

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('bike','service_type','booking_date','booking_time','status','price','notes')
        widgets = {
            'booking_date': forms.DateInput(attrs={'type':'date'}),
            'booking_time': forms.TimeInput(attrs={'type':'time'}),
            'notes': forms.Textarea(attrs={'rows':2, 'placeholder':'หมายเหตุเพิ่มเติม (ถ้ามี)'}),
        }

    def clean_booking_date(self):
        import datetime
        booking_date = self.cleaned_data['booking_date']
        if booking_date < datetime.date.today():
            raise forms.ValidationError('ไม่สามารถจองย้อนหลังได้ (Cannot book in the past)')
        return booking_date

    def clean(self):
        cleaned_data = super().clean()
        bike = cleaned_data.get('bike')
        booking_date = cleaned_data.get('booking_date')
        booking_time = cleaned_data.get('booking_time')
        if bike and booking_date and booking_time:
            exists = Booking.objects.filter(bike=bike, booking_date=booking_date, booking_time=booking_time)
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)
            if exists.exists():
                raise forms.ValidationError('มีการจองรถคันนี้ในวันและเวลาเดียวกันแล้ว (Duplicate booking for this bike, date, and time)')
        return cleaned_data
