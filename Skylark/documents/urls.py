from django.urls import path
from .views import DocumentDetailView

urlpatterns = [path("<uuid:document_id>/", DocumentDetailView.as_view(), name="document-detail")]
