from rest_framework import serializers
from .models import ExportJob

class ExportJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportJob
        fields = ["id", "document_id", "status", "artifact_key", "created_at", "completed_at"]
