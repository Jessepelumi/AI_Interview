from django.urls import path

from .views import OrderCreateView

urlpatterns = [
    path(
        "portfolios/<int:portfolio_id>/orders/",
        OrderCreateView.as_view(),
        name="order-create",
    )
]
