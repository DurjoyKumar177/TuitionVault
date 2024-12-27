from rest_framework import generics, permissions
from tutions.models import TuitionApplication
from .serializers import TuitionApplicationSerializer

class MyApplicationsView(generics.ListAPIView):
    """View for listing a user's applications."""
    serializer_class = TuitionApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TuitionApplication.objects.filter(user=self.request.user)

class MyApprovedTuitionsView(generics.ListAPIView):
    """View for listing a user's approved tuitions."""
    serializer_class = TuitionApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TuitionApplication.objects.filter(user=self.request.user, is_approved=True)
