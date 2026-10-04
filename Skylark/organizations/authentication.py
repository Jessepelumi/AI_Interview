from rest_framework import authentication, exceptions
from .models import Membership

class HeaderMembershipAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        user_id = request.headers.get("X-User-ID")
        workspace = request.headers.get("X-Workspace")
        if not user_id or not workspace:
            return None
        try:
            membership = Membership.objects.select_related("workspace", "user").get(
                user_id=user_id, workspace__slug=workspace, active=True
            )
        except Membership.DoesNotExist as exc:
            raise exceptions.AuthenticationFailed("Active workspace membership required") from exc
        return membership, None
