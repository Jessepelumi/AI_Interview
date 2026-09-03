from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account

from .serializers import TransferCreateSerializer, TransferSerializer


class TransferCreateView(APIView):
    def post(self, request, account_id):
        account = Account.objects.select_related("organisation").get(pk=account_id)
        serializer = TransferCreateSerializer(
            data=request.data, context={"account": account}
        )
        serializer.is_valid(raise_exception=True)
        transfer = serializer.save()
        return Response(TransferSerializer(transfer).data, status=status.HTTP_201_CREATED)
