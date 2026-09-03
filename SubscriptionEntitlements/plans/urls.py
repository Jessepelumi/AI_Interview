from django.urls import path

from .views import PlanDetailView

urlpatterns = [path("plans/<slug:slug>/", PlanDetailView.as_view(), name="plan-detail")]
