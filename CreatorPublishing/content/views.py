from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer, ScheduleSerializer
from .services import schedule_post


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.select_related("workspace", "author").order_by("id")


class SchedulePostView(APIView):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        serializer = ScheduleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        schedule_post(post, serializer.validated_data["scheduled_at"])
        return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
