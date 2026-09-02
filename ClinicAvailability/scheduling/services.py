from django.db.models import Count, F, Q

from .models import Slot


def available_slots(clinic, day):
    """Return slots with remaining capacity on a local calendar date."""
    return (
        Slot.objects.filter(clinic=clinic, starts_at__date=day)
        .annotate(booked_count=Count("bookings", filter=Q(bookings__status="confirmed")))
        .filter(booked_count__lt=F("capacity"))
        .order_by("starts_at")
    )

