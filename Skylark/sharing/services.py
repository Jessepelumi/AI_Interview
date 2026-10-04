from django.core.cache import cache
from django.db import transaction
from django.db.models import F
from directory.services import group_subjects
from .models import Grant

ACCESS_CACHE_TTL = 600

def _access_key(membership, document):
    return f"document-access:{document.id}:user:{membership.user_id}"

def can_view(membership, document):
    key = _access_key(membership, document)
    cached = cache.get(key)
    if cached is not None:
        return cached
    allowed = document.owner_id == membership.id
    if not allowed:
        subjects = [str(membership.id), *group_subjects(membership)]
        allowed = Grant.objects.filter(document=document, active=True, principal_id__in=subjects).exists()
    cache.set(key, allowed, ACCESS_CACHE_TTL)
    return allowed

@transaction.atomic
def create_grant(document, principal_type, principal_id):
    grant, _ = Grant.objects.update_or_create(
        document=document,
        principal_type=principal_type,
        principal_id=str(principal_id),
        defaults={"active": True},
    )
    document.acl_version = F("acl_version") + 1
    document.save(update_fields=["acl_version"])
    document.refresh_from_db()
    return grant

@transaction.atomic
def revoke_grant(grant):
    grant = Grant.objects.select_for_update().select_related("document").get(pk=grant.pk)
    if not grant.active:
        return grant
    grant.active = False
    grant.save(update_fields=["active"])
    grant.document.acl_version = F("acl_version") + 1
    grant.document.save(update_fields=["acl_version"])
    grant.document.refresh_from_db()
    return grant
