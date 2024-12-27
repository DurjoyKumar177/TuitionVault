from django.contrib import admin
from .models import TuitionReview

@admin.register(TuitionReview)
class TuitionReviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'reviewer', 'rating', 'reviewed_at')
    search_fields = ('application__tuition_post__title', 'reviewer__username')
