from rest_framework import generics, permissions
from .models import TuitionReview
from .serializers import TuitionReviewSerializer

class TuitionReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = TuitionReview.objects.all()
    serializer_class = TuitionReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Restrict reviews to the ones created by the authenticated user
        return TuitionReview.objects.filter(reviewer=self.request.user)

class TuitionReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TuitionReview.objects.all()
    serializer_class = TuitionReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Restrict to reviews created by the authenticated user
        return TuitionReview.objects.filter(reviewer=self.request.user)
