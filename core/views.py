# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.db.models import Count, Q

from .forms import RegisterForm, MotorbikeForm, BookingForm
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
def is_mechanic(user):
    return user.groups.filter(name='mechanic').exists() or user.is_superuser

# Mechanic dashboard: see all bookings, update status, set pickup date
@login_required
@user_passes_test(is_mechanic)
def mechanic_dashboard(request):
    bookings = Booking.objects.select_related('bike', 'user').order_by('-booking_date', '-booking_time')
    return render(request, 'core/mechanic_dashboard.html', {'bookings': bookings})

# Mechanic updates booking status and pickup date
@login_required
@user_passes_test(is_mechanic)
def mechanic_update_status(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'in_progress':
            booking.status = 'in_progress'
            booking.mechanic = request.user
            booking.save()
            messages.success(request, f'Booking #{booking.id} กำลังซ่อม')
        elif action == 'done':
            pickup_date = request.POST.get('pickup_date')
            if pickup_date:
                booking.pickup_date = pickup_date
            booking.status = 'done'
            booking.mechanic = request.user
            booking.save()
            messages.success(request, f'Booking #{booking.id} ซ่อมเสร็จแล้ว')
        # TODO: notify user (future step)
        return HttpResponseRedirect(reverse('mechanic_dashboard'))
    return HttpResponseForbidden()
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
    # admin เห็นทุก booking, user เห็นเฉพาะของตัวเอง
    if request.user.is_superuser or request.user.is_staff:
        bookings = Booking.objects.select_related('bike', 'user')
    else:
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
    paginate_by = 7

    def get_queryset(self):
        qs = Motorbike.objects.filter(owner=self.request.user)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(brand__icontains=q) |
                Q(model__icontains=q) |
                Q(plate_number__icontains=q)
            )
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context

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
    paginate_by = 7

    def get_queryset(self):
        user = self.request.user
        qs = Booking.objects.select_related('bike', 'user') if (user.is_superuser or user.is_staff) else Booking.objects.filter(user=user).select_related('bike')
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        if q:
            qs = qs.filter(
                Q(bike__brand__icontains=q) |
                Q(bike__model__icontains=q) |
                Q(service_type__icontains=q)
            )
        if status:
            qs = qs.filter(status=status)
        return qs.order_by('-booking_date', '-booking_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['status'] = self.request.GET.get('status', '')
        context['status_choices'] = Booking.STATUS_CHOICES
        return context

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
