from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Grant
from documents.models import Document
from .serializers import CreateGrantSerializer, RevokeGrantSerializer
from .services import create_grant, revoke_grant

class CreateGrantView(APIView):
    def post(self, request):
        serializer = CreateGrantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = get_object_or_404(Document, id=serializer.validated_data["document_id"], workspace=request.user.workspace)
        if document.owner_id != request.user.id and request.user.role != "admin":
            return Response({"detail": "Forbidden"}, status=403)
        grant = create_grant(document, serializer.validated_data["principal_type"], serializer.validated_data["principal_id"])
        return Response({"id": grant.id}, status=201)

class RevokeGrantView(APIView):
    def post(self, request):
        serializer = RevokeGrantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        grant = get_object_or_404(Grant.objects.select_related("document"), pk=serializer.validated_data["grant_id"], document__workspace=request.user.workspace)
        if grant.document.owner_id != request.user.id and request.user.role != "admin":
            return Response({"detail": "Forbidden"}, status=403)
        revoke_grant(grant)
        return Response(status=204)
