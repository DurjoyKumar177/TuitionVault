from rest_framework import serializers
from tutions.models import TuitionApplication

class TuitionApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuitionApplication
        fields = ['id', 'tuition_post', 'user', 'applied_at', 'is_approved']
