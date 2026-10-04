from django.urls import include, path

urlpatterns = [
    path("api/documents/", include("documents.urls")),
    path("api/sharing/", include("sharing.urls")),
    path("api/search/", include("search_index.urls")),
    path("api/exports/", include("exports.urls")),
]
