from django.urls import path
from .views import CreateGrantView, RevokeGrantView

urlpatterns = [
    path("grants/", CreateGrantView.as_view(), name="grant-create"),
    path("revoke/", RevokeGrantView.as_view(), name="grant-revoke"),
]
