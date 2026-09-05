from django.urls import include, path

urlpatterns = [
    path("api/", include("beneficiaries.urls")),
    path("api/", include("transfers.urls")),
]
