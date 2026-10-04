from django.urls import path
from .views import ExportCreateView

urlpatterns = [path("documents/<uuid:document_id>/", ExportCreateView.as_view(), name="export-create")]
