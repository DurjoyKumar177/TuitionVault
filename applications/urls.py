from django.urls import path
from .views import MyApplicationsView, MyApprovedTuitionsView, ApplicationHistoryView

urlpatterns = [
    path('my-applications/', MyApplicationsView.as_view(), name='my-applications'),
    path('my-approved-tuitions/', MyApprovedTuitionsView.as_view(), name='my-approved-tuitions'),
    path('history/', ApplicationHistoryView.as_view(), name='application-history'),
]
