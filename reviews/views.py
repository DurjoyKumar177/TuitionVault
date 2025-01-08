from rest_framework import generics, permissions
from .models import TuitionReview
from .serializers import TuitionReviewSerializer

class CreateReviewAPIView(generics.CreateAPIView):
    serializer_class = TuitionReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

class ViewReviewAPIView(generics.ListAPIView):
    serializer_class = TuitionReviewSerializer

    def get_queryset(self):
        tuition_post_id = self.kwargs.get('tuition_post_id')
        return TuitionReview.objects.filter(application__tuition_post_id=tuition_post_id)
