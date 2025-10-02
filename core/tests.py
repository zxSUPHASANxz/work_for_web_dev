from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Motorbike, Booking
from django.utils import timezone
import datetime

class UserBikeBookingTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
		self.client.login(username='testuser', password='testpass')

	def test_register_user(self):
		user_count = User.objects.count()
		self.assertEqual(user_count, 1)
		self.assertEqual(self.user.email, 'test@example.com')

	def test_add_bike(self):
		bike = Motorbike.objects.create(owner=self.user, brand='Honda', model='Wave', plate_number='1234', year=2020)
		self.assertEqual(Motorbike.objects.count(), 1)
		self.assertEqual(bike.brand, 'Honda')

	def test_booking_no_past(self):
		from core.forms import BookingForm
		bike = Motorbike.objects.create(owner=self.user, brand='Yamaha', model='Mio', plate_number='5678', year=2021)
		past_date = timezone.now().date() - datetime.timedelta(days=1)
		form = BookingForm(data={
			'bike': bike.id,
			'service_type': 'Oil Change',
			'booking_date': past_date,
			'booking_time': '10:00',
			'status': 'pending',
		})
		self.assertFalse(form.is_valid())
		self.assertIn('booking_date', form.errors)

	def test_booking_no_duplicate(self):
		bike = Motorbike.objects.create(owner=self.user, brand='Suzuki', model='Smash', plate_number='9999', year=2022)
		today = timezone.now().date() + datetime.timedelta(days=1)
		Booking.objects.create(user=self.user, bike=bike, service_type='Check', booking_date=today, booking_time='11:00')
		with self.assertRaises(Exception):
			Booking.objects.create(user=self.user, bike=bike, service_type='Check', booking_date=today, booking_time='11:00')
