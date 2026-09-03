from django.urls import path

from .views import BeneficiaryListCreateView

urlpatterns = [
    path("beneficiaries/", BeneficiaryListCreateView.as_view(), name="beneficiaries")
]
