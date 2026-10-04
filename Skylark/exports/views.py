from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from documents.models import Document
from .serializers import ExportJobSerializer
from .services import request_export

class ExportCreateView(APIView):
    def post(self, request, document_id):
        document = get_object_or_404(Document, id=document_id, workspace=request.user.workspace, status=Document.Status.ACTIVE)
        try:
            job = request_export(request.user, document)
        except PermissionError:
            return Response({"detail": "Not found."}, status=404)
        return Response(ExportJobSerializer(job).data, status=202)
