from django.urls import path

from .views import provider_webhook

urlpatterns = [path("webhooks/provider/", provider_webhook, name="provider-webhook")]

