from rest_framework import serializers
from .models import TuitionReview, TuitionApplication

class TuitionReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)  # Added reviewer name

    class Meta:
        model = TuitionReview
        fields = ['id', 'rating', 'comment', 'reviewer_name', 'reviewed_at']  # Include reviewer_name
        read_only_fields = ['reviewed_at']

    def validate(self, data):
        request = self.context['request']
        user = request.user

        try:
            application = TuitionApplication.objects.get(
                tuition_post_id=self.context['view'].kwargs.get('tuition_post_id'),
                user=user,
                is_approved=True
            )
        except TuitionApplication.DoesNotExist:
            raise serializers.ValidationError("You can only review your own approved tuition applications.")

        data['application'] = application
        return data
