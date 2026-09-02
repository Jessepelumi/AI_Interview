from django.urls import path

from .views import clinic_availability

urlpatterns = [
    path(
        "clinics/<slug:clinic_slug>/availability/",
        clinic_availability,
        name="clinic-availability",
    )
]

