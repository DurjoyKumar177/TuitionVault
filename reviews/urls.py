from django.urls import path
from .views import TuitionReviewListCreateAPIView, TuitionReviewDetailAPIView

urlpatterns = [
    path('give-review/', TuitionReviewListCreateAPIView.as_view(), name='reviews'),
    path('review/<int:pk>/', TuitionReviewDetailAPIView.as_view(), name='review-detail'),
]
