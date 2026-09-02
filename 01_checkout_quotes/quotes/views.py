import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .services import build_quote


@require_POST
def create_quote(request):
    try:
        payload = json.loads(request.body)
        quote = build_quote(payload["items"], payload.get("coupon_code"))
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return JsonResponse({"error": "invalid quote request"}, status=400)

    return JsonResponse(
        {
            "subtotal": f"{quote.subtotal:.2f}",
            "discount": f"{quote.discount:.2f}",
            "total": f"{quote.total:.2f}",
        }
    )

