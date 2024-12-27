from django.urls import path
from .views import MyApplicationsView, MyApprovedTuitionsView

urlpatterns = [
    path('my-applications/', MyApplicationsView.as_view(), name='my-applications'),
    path('my-approved-tuitions/', MyApprovedTuitionsView.as_view(), name='my-approved-tuitions'),
]
