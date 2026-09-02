from datetime import date, datetime

from django.test import TestCase
from django.utils import timezone

from .models import Booking, Clinic, Slot
from .services import available_slots


def at(hour):
    return timezone.make_aware(datetime(2026, 9, 8, hour, 0))


class AvailabilityServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.north = Clinic.objects.create(name="North Clinic", slug="north")
        cls.south = Clinic.objects.create(name="South Clinic", slug="south")

    def test_slots_from_another_clinic_never_leak(self):
        north_slot = Slot.objects.create(
            clinic=self.north, starts_at=at(9), capacity=1
        )
        Slot.objects.create(clinic=self.south, starts_at=at(10), capacity=1)

        result = list(available_slots(self.north, date(2026, 9, 8)))

        self.assertEqual(result, [north_slot])

    def test_cancelled_booking_does_not_consume_capacity(self):
        slot = Slot.objects.create(clinic=self.north, starts_at=at(11), capacity=1)
        Booking.objects.create(
            slot=slot, patient_name="Asha", status=Booking.Status.CANCELLED
        )

        result = list(available_slots(self.north, date(2026, 9, 8)))

        self.assertEqual(result, [slot])
        self.assertEqual(result[0].booked_count, 0)

    def test_confirmed_bookings_consume_capacity(self):
        full_slot = Slot.objects.create(
            clinic=self.north, starts_at=at(12), capacity=1
        )
        Booking.objects.create(
            slot=full_slot, patient_name="Ben", status=Booking.Status.CONFIRMED
        )

        self.assertNotIn(
            full_slot, available_slots(self.north, date(2026, 9, 8))
        )


class AvailabilityApiTests(TestCase):
    def test_response_is_ordered_and_reports_remaining_capacity(self):
        clinic = Clinic.objects.create(name="Central Clinic", slug="central")
        later = Slot.objects.create(clinic=clinic, starts_at=at(15), capacity=3)
        earlier = Slot.objects.create(clinic=clinic, starts_at=at(14), capacity=2)
        Booking.objects.create(
            slot=earlier, patient_name="Cleo", status=Booking.Status.CONFIRMED
        )

        response = self.client.get(
            "/api/clinics/central/availability/", {"date": "2026-09-08"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [slot["id"] for slot in response.json()["slots"]],
            [earlier.id, later.id],
        )
        self.assertEqual(response.json()["slots"][0]["remaining"], 1)

    def test_invalid_date_returns_400(self):
        Clinic.objects.create(name="Central Clinic", slug="central")

        response = self.client.get(
            "/api/clinics/central/availability/", {"date": "08/09/2026"}
        )

        self.assertEqual(response.status_code, 400)

