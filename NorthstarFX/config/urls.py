from django.urls import include, path
urlpatterns = [path("api/", include("quotes.urls")), path("api/", include("conversions.urls"))]
