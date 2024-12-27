from rest_framework import serializers
from .models import TuitionReview


class TuitionReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TuitionReview
        fields = ['id', 'application', 'reviewer', 'rating', 'comment', 'reviewed_at']
        read_only_fields = ['reviewed_at']

    def validate(self, data):
        application = data.get('application')

        # Ensure the application belongs to the user
        if application.user != self.context['request'].user:
            raise serializers.ValidationError("You can only review your own approved tuition applications.")

        # Ensure the application is approved
        if not application.is_approved:
            raise serializers.ValidationError("You cannot review a tuition application that is not approved.")

        # Ensure the review doesn't already exist
        if TuitionReview.objects.filter(application=application).exists():
            raise serializers.ValidationError("A review for this tuition has already been submitted.")

        return data
