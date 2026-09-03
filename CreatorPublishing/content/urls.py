from django.urls import path

from .views import PostListCreateView, SchedulePostView

urlpatterns = [
    path("posts/", PostListCreateView.as_view(), name="posts"),
    path("posts/<int:post_id>/schedule/", SchedulePostView.as_view(), name="schedule-post"),
]
