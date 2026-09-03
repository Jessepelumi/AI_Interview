from django.urls import path

from .views import billing_webhook

urlpatterns = [
    path("billing/<str:provider>/", billing_webhook, name="billing-webhook")
]
