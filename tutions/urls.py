from django.urls import path
from .views import TuitionPostListAPIView, TuitionPostDetailAPIView, TuitionPostFilterByClassAPIView, TuitionPostFilterByLocationAPIView, TuitionPostFilterByPaymentAPIView, TuitionPostSearchByTitleAPIView

urlpatterns = [
    path('posts/', TuitionPostListAPIView.as_view(), name='tuition-post-list'),
    path('posts_details/<int:pk>/', TuitionPostDetailAPIView.as_view(), name='tuition-post-detail'),
    path('filter_by_class/', TuitionPostFilterByClassAPIView.as_view(), name='tuition-post-filter-class'),
    path('filter_by_location/', TuitionPostFilterByLocationAPIView.as_view(), name='tuition-post-filter-location'),
    path('filter_by_payment/', TuitionPostFilterByPaymentAPIView.as_view(), name='tuition-post-filter-payment'),
    path('search_by_title/', TuitionPostSearchByTitleAPIView.as_view(), name='tuition-post-search-title'),
]
