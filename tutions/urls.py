from django.urls import path
from .views import TuitionPostListAPIView,ApplyForTuitionAPIView, TuitionPostDetailAPIView, TuitionPostFilterByClassAPIView, TuitionPostFilterByLocationAPIView, TuitionPostFilterByPaymentAPIView, TuitionPostSearchByTitleAPIView, DropdownOptionsAPIView

urlpatterns = [
    path('posts/', TuitionPostListAPIView.as_view(), name='tuition-post-list'),
    path('posts_details/<int:pk>/', TuitionPostDetailAPIView.as_view(), name='tuition-post-detail'),
    path('filter_by_class/', TuitionPostFilterByClassAPIView.as_view(), name='tuition-post-filter-class'),
    path('filter_by_location/', TuitionPostFilterByLocationAPIView.as_view(), name='tuition-post-filter-location'),
    path('filter_by_payment/', TuitionPostFilterByPaymentAPIView.as_view(), name='tuition-post-filter-payment'),
    path('search_by_title/', TuitionPostSearchByTitleAPIView.as_view(), name='tuition-post-search-title'),
    path('dropdown_options/<str:field>/', DropdownOptionsAPIView.as_view(), name='dropdown-options'),
    path('apply/<int:tuition_post_id>/', ApplyForTuitionAPIView.as_view(), name='apply_for_tuition_api'),
]
