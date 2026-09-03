from rest_framework import generics

from .models import Plan
from .serializers import PlanSerializer


class PlanDetailView(generics.RetrieveAPIView):
    queryset = Plan.objects.prefetch_related("feature_rules__feature")
    serializer_class = PlanSerializer
    lookup_field = "slug"
