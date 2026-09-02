from django.db.models import Count, F

from .models import Slot


def available_slots(clinic, day):
    """Return slots with remaining capacity on a local calendar date."""
    return (
        Slot.objects.filter(starts_at__date=day)
        .annotate(booked_count=Count("bookings"))
        .filter(booked_count__lt=F("capacity"))
        .order_by("starts_at")
    )

