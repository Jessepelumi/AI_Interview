from rest_framework import viewsets
from .models import Quote
from .serializers import QuoteSerializer
class QuoteViewSet(viewsets.ModelViewSet):
    serializer_class = QuoteSerializer
    http_method_names = ["get", "post", "head", "options"]
    def get_queryset(self):
        return Quote.objects.filter(customer__users=self.request.user).order_by("-created_at")
