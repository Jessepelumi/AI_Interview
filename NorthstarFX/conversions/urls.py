from django.urls import path
from .views import BookQuoteView
urlpatterns = [path("quotes/<uuid:quote_id>/book/", BookQuoteView.as_view(), name="book-quote")]
