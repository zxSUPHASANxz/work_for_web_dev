"""
URL configuration for motorbike_booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# motorbike_booking/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView

from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/logout/', LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout/password
    path('register/', core_views.register, name='register'),
    path('register/mechanic/', core_views.register_mechanic, name='register_mechanic'),
    path('', core_views.home, name='home'),
    path('dashboard/', core_views.dashboard, name='dashboard'),
    path('login/mechanic/', LoginView.as_view(template_name='registration/login_mechanic.html'), name='login_mechanic'),
    # Mechanic dashboard and actions
    path('mechanic/dashboard/', core_views.mechanic_dashboard, name='mechanic_dashboard'),
    path('mechanic/booking/<int:booking_id>/update/', core_views.mechanic_update_status, name='mechanic_update_status'),
    # Profile pages
    path('profile/', core_views.user_profile, name='user_profile'),
    path('mechanic/profile/', core_views.mechanic_profile, name='mechanic_profile'),
    # Motorbikes
    path('bikes/', core_views.BikeListView.as_view(), name='bike_list'),
    path('bikes/add/', core_views.BikeCreateView.as_view(), name='bike_add'),
    path('bikes/<int:pk>/edit/', core_views.BikeUpdateView.as_view(), name='bike_edit'),
    path('bikes/<int:pk>/delete/', core_views.BikeDeleteView.as_view(), name='bike_delete'),
    # Bookings
    path('bookings/', core_views.BookingListView.as_view(), name='booking_list'),
    path('bookings/add/', core_views.BookingCreateView.as_view(), name='booking_add'),
    path('bookings/<int:pk>/edit/', core_views.BookingUpdateView.as_view(), name='booking_edit'),
    path('bookings/<int:pk>/delete/', core_views.BookingDeleteView.as_view(), name='booking_delete'),
]

