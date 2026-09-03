from django.urls import path

from .views import ReturnCreateView

urlpatterns = [path("returns/", ReturnCreateView.as_view(), name="return-create")]
