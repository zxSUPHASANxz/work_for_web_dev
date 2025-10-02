# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Motorbike, Booking

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
        fields = ('bike','service_type','booking_date','booking_time','status')
        widgets = {
            'booking_date': forms.DateInput(attrs={'type':'date'}),
            'booking_time': forms.TimeInput(attrs={'type':'time'}),
        }
