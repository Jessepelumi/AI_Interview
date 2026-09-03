from rest_framework import decorators, response, status, viewsets
from accounts.models import Membership
from .models import Dispute
from .serializers import DisputeSerializer
from .services import transition

class DisputeViewSet(viewsets.ModelViewSet):
    serializer_class = DisputeSerializer
    queryset = Dispute.objects.all().order_by("-created_at")
    def get_queryset(self):
        organisation_ids = Membership.objects.filter(user=self.request.user).values_list("organisation_id", flat=True)
        if self.action == "list":
            return self.queryset.filter(organisation_id__in=organisation_ids).select_related("payment")
        return self.queryset
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    @decorators.action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        dispute = self.get_object()
        try:
            transition(dispute, Dispute.State.SUBMITTED, request.user)
        except Exception:
            return response.Response({"detail": "Unable to submit dispute"}, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(self.get_serializer(dispute).data)
