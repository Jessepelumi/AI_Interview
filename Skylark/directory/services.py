from django.core.cache import cache
from .models import GroupMember

GROUP_CACHE_TTL = 900

def group_subjects(membership):
    # Directory identities are cached to absorb bursts from document listing and search.
    key = f"directory-groups:user:{membership.user_id}"
    cached = cache.get(key)
    if cached is not None:
        return cached
    external_ids = list(
        GroupMember.objects.filter(membership=membership).values_list("group__external_id", flat=True)
    )
    cache.set(key, external_ids, GROUP_CACHE_TTL)
    return external_ids
