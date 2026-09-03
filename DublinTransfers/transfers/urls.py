from django.urls import path

from .views import TransferCreateView

urlpatterns = [
    path(
        "accounts/<uuid:account_id>/transfers/",
        TransferCreateView.as_view(),
        name="transfer-create",
    )
]
