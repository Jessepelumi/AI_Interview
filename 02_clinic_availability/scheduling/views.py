from datetime import date

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

from .models import Clinic
from .services import available_slots


@require_GET
def clinic_availability(request, clinic_slug):
    clinic = get_object_or_404(Clinic, slug=clinic_slug)
    try:
        requested_day = date.fromisoformat(request.GET["date"])
    except (KeyError, ValueError):
        return JsonResponse({"error": "date must use YYYY-MM-DD"}, status=400)

    slots = available_slots(clinic, requested_day)
    return JsonResponse(
        {
            "clinic": clinic.slug,
            "slots": [
                {
                    "id": slot.id,
                    "starts_at": slot.starts_at.isoformat(),
                    "remaining": slot.capacity - slot.booked_count,
                }
                for slot in slots
            ],
        }
    )

