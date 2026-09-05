from rest_framework import generics

from .models import Beneficiary
from .serializers import BeneficiarySerializer


class BeneficiaryListCreateView(generics.ListCreateAPIView):
    queryset = Beneficiary.objects.select_related("organisation").all()
    serializer_class = BeneficiarySerializer
