from django.urls import include, path

urlpatterns = [
    path("api/", include("plans.urls")),
    path("webhooks/", include("integrations.urls")),
]
