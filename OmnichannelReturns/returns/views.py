from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ReturnCreateSerializer, ReturnSerializer


class ReturnCreateView(APIView):
    def post(self, request):
        serializer = ReturnCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return_request = serializer.save()
        return Response(ReturnSerializer(return_request).data, status=status.HTTP_201_CREATED)
