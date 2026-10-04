from directory.services import group_subjects
from sharing.models import Grant
from .events import IndexEvent
from .models import IndexedDocument

def build_index_event(document):
    subjects = list(Grant.objects.filter(document=document, active=True).values_list("principal_id", flat=True))
    return IndexEvent(str(document.id), document.acl_version, document.title, subjects)

def apply_index_event(payload):
    IndexedDocument.objects.update_or_create(
        document_id=payload["document_id"],
        defaults={"title": payload["title"], "acl_version": payload["acl_version"], "allowed_subjects": payload["allowed_subjects"]},
    )

def search_for(membership, query):
    subjects = {str(membership.id), *group_subjects(membership)}
    records = IndexedDocument.objects.filter(document__workspace=membership.workspace, document__status="active", title__icontains=query)
    return [record.document for record in records if subjects.intersection(record.allowed_subjects) or record.document.owner_id == membership.id]
