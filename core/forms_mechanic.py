from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MechanicProfile

class MechanicRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, label='เบอร์โทรศัพท์')
    experience = forms.IntegerField(min_value=0, label='ประสบการณ์ (ปี)')
    shop_name = forms.CharField(max_length=100, label='ชื่อร้าน/อู่')
    shop_address = forms.CharField(max_length=255, label='ที่อยู่ร้าน')

    class Meta:
        model = User
        fields = ('username','email','password1','password2','phone','experience','shop_name','shop_address')
