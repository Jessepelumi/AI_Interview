from rest_framework import status, views
from rest_framework.response import Response
from quotes.models import Quote
from .services import book_quote
class BookQuoteView(views.APIView):
    def post(self, request, quote_id):
        quote = Quote.objects.get(id=quote_id)
        if not quote.customer.users.filter(id=request.user.id).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        key = request.headers.get("Idempotency-Key", "")
        try:
            conversion, created = book_quote(quote, key)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)
        return Response({"id": conversion.id, "created": created}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
