from django.urls import path

from .views import create_quote

urlpatterns = [path("quotes/", create_quote, name="create-quote")]

