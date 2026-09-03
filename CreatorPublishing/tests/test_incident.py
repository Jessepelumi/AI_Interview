from datetime import UTC, datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory

from content.models import Post
from content.serializers import PostSerializer
from content.services import schedule_post
from integrations.client import ChannelRequestBuilder
from integrations.models import ChannelConnection
from moderation.models import ModerationDecision
from moderation.services import apply_provider_decision
from publishing.services import record_publication
from workspaces.models import Workspace


class CreatorPublishingIncidentTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("niamh")
        self.other = get_user_model().objects.create_user("other")
        self.workspace = Workspace.objects.create(
            name="Dublin Food", timezone_name="Europe/Dublin"
        )
        self.workspace.members.add(self.user)
        self.other_workspace = Workspace.objects.create(
            name="Private Launches", timezone_name="America/New_York"
        )
        self.other_workspace.members.add(self.other)

    def make_post(self, workspace=None, author=None, status=Post.Status.APPROVED):
        return Post.objects.create(
            workspace=workspace or self.workspace,
            author=author or self.user,
            body="Doors open at nine",
            status=status,
        )

    def test_dublin_summer_schedule_preserves_instant(self):
        post = self.make_post()
        # API input 09:00+01 is already normalised by DRF to 08:00 UTC.
        requested = datetime(2026, 6, 15, 8, 0, tzinfo=UTC)
        schedule_post(post, requested)
        self.assertEqual(post.scheduled_for, requested)

    def test_provider_allow_maps_to_approved_model_outcome(self):
        post = self.make_post(status=Post.Status.DRAFT)
        decision = apply_provider_decision(post, "allow")
        post.refresh_from_db()
        self.assertEqual(decision.outcome, ModerationDecision.Outcome.APPROVED)
        self.assertEqual(post.status, Post.Status.APPROVED)

    def test_post_list_is_scoped_to_users_workspaces(self):
        own = self.make_post()
        self.make_post(workspace=self.other_workspace, author=self.other)
        client = APIClient()
        client.force_authenticate(self.user)
        response = client.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.data], [own.id])

    def test_publish_request_uses_workspace_connection_token(self):
        post = self.make_post()
        connection = ChannelConnection.objects.create(
            workspace=self.workspace,
            channel="photo-app",
            access_token="workspace-secret-token",
            remote_account_id="remote-77",
        )
        request = ChannelRequestBuilder(connection).build_publish_request(post)
        self.assertEqual(
            request["headers"]["Authorization"], "Bearer workspace-secret-token"
        )

    def test_winter_schedule_is_unchanged_for_dublin(self):
        post = self.make_post()
        requested = datetime(2026, 1, 15, 9, 0, tzinfo=UTC)
        schedule_post(post, requested)
        self.assertEqual(post.scheduled_for, requested)

    def test_serializer_maps_public_caption_to_internal_body(self):
        request = APIRequestFactory().post("/api/posts/")
        request.user = self.user
        serializer = PostSerializer(
            data={"workspace_id": self.workspace.id, "caption": "New menu"},
            context={"request": request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        post = serializer.save()
        self.assertEqual(post.body, "New menu")

    def test_rejected_post_cannot_be_scheduled(self):
        post = self.make_post(status=Post.Status.REJECTED)
        with self.assertRaisesMessage(ValueError, "only approved"):
            schedule_post(post, datetime(2026, 1, 1, 9, tzinfo=UTC))

    def test_publication_recording_is_idempotent_per_channel(self):
        post = self.make_post()
        first = record_publication(post, "photo-app", "remote-1")
        second = record_publication(post, "photo-app", "remote-2")
        self.assertEqual(first.id, second.id)
