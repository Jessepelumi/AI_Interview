from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from sharing.services import can_view
from .models import Document
from .serializers import DocumentSerializer

class DocumentDetailView(APIView):
    def get(self, request, document_id):
        document = get_object_or_404(Document, id=document_id, workspace=request.user.workspace, status=Document.Status.ACTIVE)
        if not can_view(request.user, document):
            return Response({"detail": "Not found."}, status=404)
        return Response(DocumentSerializer(document).data)
