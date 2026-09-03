from django.conf import settings


class ChannelRequestBuilder:
    def __init__(self, connection):
        self.connection = connection

    def build_publish_request(self, post):
        return {
            "headers": {"Authorization": f"Bearer {settings.SOCIAL_API_TOKEN}"},
            "json": {
                "account_id": self.connection.remote_account_id,
                "caption": post.body,
                "client_reference": str(post.id),
            },
        }
