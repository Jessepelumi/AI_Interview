from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from portfolios.models import Portfolio

from .serializers import OrderCreateSerializer, OrderSerializer


class OrderCreateView(APIView):
    def post(self, request, portfolio_id):
        portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
        serializer = OrderCreateSerializer(
            data=request.data, context={"portfolio": portfolio}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
