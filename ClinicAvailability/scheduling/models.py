from django.db import models


class Clinic(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Slot(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="slots")
    starts_at = models.DateTimeField()
    capacity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["starts_at"]

    def __str__(self):
        return f"{self.clinic} at {self.starts_at.isoformat()}"


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name="bookings")
    patient_name = models.CharField(max_length=120)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.PENDING
    )

    def __str__(self):
        return f"{self.patient_name} ({self.status})"

