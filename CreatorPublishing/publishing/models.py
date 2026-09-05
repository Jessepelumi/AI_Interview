from django.db import models

from content.models import Post


class Publication(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="publications")
    channel = models.CharField(max_length=24)
    remote_id = models.CharField(max_length=120)
    published_at = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post", "channel"], name="one_publication_per_post_channel"
            )
        ]
