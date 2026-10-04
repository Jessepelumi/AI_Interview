from rest_framework.response import Response
from rest_framework.views import APIView
from documents.serializers import DocumentSerializer
from .serializers import SearchQuerySerializer
from .services import search_for

class SearchView(APIView):
    def get(self, request):
        serializer = SearchQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        documents = search_for(request.user, serializer.validated_data["q"])
        return Response({"results": DocumentSerializer(documents, many=True).data})
