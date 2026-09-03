from django.utils import timezone

from content.models import Post

from .models import Publication


def record_publication(post, channel, remote_id, published_at=None):
    publication, _ = Publication.objects.get_or_create(
        post=post,
        channel=channel,
        defaults={
            "remote_id": remote_id,
            "published_at": published_at or timezone.now(),
        },
    )
    post.status = Post.Status.PUBLISHED
    post.save(update_fields=["status"])
    return publication
