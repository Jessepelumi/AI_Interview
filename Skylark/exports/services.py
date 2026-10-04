from django.utils import timezone
from sharing.services import can_view
from .models import ExportJob

def request_export(membership, document):
    if not can_view(membership, document):
        raise PermissionError("document access required")
    return ExportJob.objects.create(document=document, requested_by=membership)

def execute_export(job_id):
    job = ExportJob.objects.select_related("document", "requested_by").get(pk=job_id)
    if job.status != ExportJob.Status.QUEUED:
        return job
    job.status = ExportJob.Status.COMPLETE
    job.artifact_key = f"exports/{job.document_id}/{job.id}.pdf"
    job.completed_at = timezone.now()
    job.save(update_fields=["status", "artifact_key", "completed_at"])
    return job
