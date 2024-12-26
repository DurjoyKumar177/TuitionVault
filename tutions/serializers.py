from rest_framework import serializers
from .models import TuitionPost, TuitionApplication

class TuitionPostSerializer(serializers.ModelSerializer):
    routine_buttons = serializers.SerializerMethodField()
    subject_buttons = serializers.SerializerMethodField()

    class Meta:
        model = TuitionPost
        fields = [
            'id', 'title', 'image', 'class_name', 'subjects', 'group', 
            'routine', 'routine_buttons', 'subject_buttons', 
            'monthly_payment', 'location', 'google_map_link', 
            'availability', 'details', 'experience', 'required_skills', 
            'created_at', 'updated_at',
        ]

    def get_routine_buttons(self, obj):
        return obj.get_routine_buttons()

    def get_subject_buttons(self, obj):
        return obj.get_subject_buttons()
    
class TuitionApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuitionApplication
        fields = []
