from rest_framework import generics, permissions
from tutions.models import TuitionApplication
from .serializers import TuitionApplicationSerializer, ApplicationHistorySerializer

class MyApplicationsView(generics.ListAPIView):
    
    serializer_class = TuitionApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TuitionApplication.objects.filter(user=self.request.user)

class MyApprovedTuitionsView(generics.ListAPIView):
    
    serializer_class = TuitionApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TuitionApplication.objects.filter(user=self.request.user, is_approved=True)
    
class ApplicationHistoryView(generics.ListAPIView):
    serializer_class = ApplicationHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TuitionApplication.objects.filter(user=self.request.user).order_by('-applied_at')
