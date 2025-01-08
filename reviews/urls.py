from django.urls import path
from .views import CreateReviewAPIView, ViewReviewAPIView

urlpatterns = [
    path('give-review/<int:tuition_post_id>/', CreateReviewAPIView.as_view(), name='create-review'),
    path('view-reviews/<int:tuition_post_id>/', ViewReviewAPIView.as_view(), name='view-reviews'),
]
