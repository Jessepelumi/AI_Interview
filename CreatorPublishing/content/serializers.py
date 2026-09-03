from rest_framework import serializers

from workspaces.models import Workspace

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    workspace_id = serializers.PrimaryKeyRelatedField(
        source="workspace", queryset=Workspace.objects.all()
    )
    caption = serializers.CharField(source="body")
    scheduled_at = serializers.DateTimeField(
        source="scheduled_for", read_only=True, allow_null=True
    )

    class Meta:
        model = Post
        fields = ("id", "workspace_id", "caption", "status", "scheduled_at")
        read_only_fields = ("id", "status", "scheduled_at")

    def create(self, validated_data):
        return Post.objects.create(author=self.context["request"].user, **validated_data)


class ScheduleSerializer(serializers.Serializer):
    scheduled_at = serializers.DateTimeField()
