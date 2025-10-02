# core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.db.models import Count

from .forms import RegisterForm, MotorbikeForm, BookingForm
from .models import Motorbike, Booking

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'สมัครสมาชิกสำเร็จ!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard(request):
    bikes = Motorbike.objects.filter(owner=request.user)
    bookings = Booking.objects.filter(user=request.user).select_related('bike')

    # นับจำนวนการจองตาม status
    status_data = (
        bookings.values("status")
        .annotate(total=Count("status"))
        .order_by("status")
    )
    labels = [s["status"] for s in status_data]
    counts = [s["total"] for s in status_data]

    return render(request, 'core/dashboard.html', {
        'bikes': bikes,
        'bookings': bookings,
        'labels': labels,
        'counts': counts,
    })

@method_decorator(login_required, name='dispatch')
class BikeListView(ListView):
    template_name = 'core/bike_list.html'
    context_object_name = 'bikes'
    def get_queryset(self):
        return Motorbike.objects.filter(owner=self.request.user)

@method_decorator(login_required, name='dispatch')
class BikeCreateView(CreateView):
    model = Motorbike
    form_class = MotorbikeForm
    template_name = 'core/bike_form.html'
    success_url = reverse_lazy('bike_list')
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        messages.success(self.request, 'เพิ่มรถเรียบร้อย')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class BikeUpdateView(UpdateView):
    model = Motorbike
    form_class = MotorbikeForm
    template_name = 'core/bike_form.html'
    success_url = reverse_lazy('bike_list')
    def get_queryset(self):
        return Motorbike.objects.filter(owner=self.request.user)
    def form_valid(self, form):
        messages.success(self.request, 'แก้ไขข้อมูลรถเรียบร้อย')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class BikeDeleteView(DeleteView):
    model = Motorbike
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('bike_list')
    def get_queryset(self):
        return Motorbike.objects.filter(owner=self.request.user)

@method_decorator(login_required, name='dispatch')
class BookingListView(ListView):
    template_name = 'core/booking_list.html'
    context_object_name = 'bookings'
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('bike')

@method_decorator(login_required, name='dispatch')
class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'core/booking_form.html'
    success_url = reverse_lazy('booking_list')
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['bike'].queryset = Motorbike.objects.filter(owner=self.request.user)
        return form
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        messages.success(self.request, 'สร้างการจองเรียบร้อย')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'core/booking_form.html'
    success_url = reverse_lazy('booking_list')
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['bike'].queryset = Motorbike.objects.filter(owner=self.request.user)
        return form
    def form_valid(self, form):
        messages.success(self.request, 'แก้ไขการจองเรียบร้อย')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('booking_list')
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
