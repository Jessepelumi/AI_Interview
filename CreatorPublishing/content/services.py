from datetime import UTC
from zoneinfo import ZoneInfo

from .models import Post


def normalise_publish_time(workspace, requested_time):
    local_wall_time = requested_time.astimezone(ZoneInfo(workspace.timezone_name))
    return local_wall_time.replace(tzinfo=UTC)


def schedule_post(post, requested_time):
    if post.status != Post.Status.APPROVED:
        raise ValueError("only approved posts may be scheduled")
    post.scheduled_for = normalise_publish_time(post.workspace, requested_time)
    post.status = Post.Status.SCHEDULED
    post.save(update_fields=["scheduled_for", "status"])
    return post
