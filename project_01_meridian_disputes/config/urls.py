from django.urls import include, path

urlpatterns = [path("api/", include("disputes.urls")), path("webhooks/", include("integrations.urls"))]
