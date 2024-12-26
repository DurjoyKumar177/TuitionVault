from django.urls import path
from .views import TuitionPostListAPIView, TuitionPostDetailAPIView, ApplyForTuitionAPIView

urlpatterns = [
    path('posts/', TuitionPostListAPIView.as_view(), name='tuition-post-list'),
    path('posts_details/<int:pk>/', TuitionPostDetailAPIView.as_view(), name='tuition-post-detail'),
    path('apply/<int:tuition_post_id>/', ApplyForTuitionAPIView.as_view(), name='apply_for_tuition_api'),
]
