from django.urls import path
from .views import processor_webhook
urlpatterns = [path("processor/", processor_webhook, name="processor-webhook")]
