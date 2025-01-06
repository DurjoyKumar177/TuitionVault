from rest_framework import serializers
from tutions.models import TuitionApplication
from tutions.serializers import TuitionPostSerializer

class TuitionApplicationSerializer(serializers.ModelSerializer):
    tuition_post = TuitionPostSerializer()
    class Meta:
        model = TuitionApplication
        fields = ['id', 'tuition_post', 'user', 'applied_at', 'is_approved',]
        
class ApplicationHistorySerializer(serializers.ModelSerializer):
    tuition_title = serializers.CharField(source='tuition_post.title', read_only=True) 

    class Meta:
        model = TuitionApplication
        fields = ['id', 'tuition_post','tuition_title', 'applied_at', 'is_approved', 'approved_at']
