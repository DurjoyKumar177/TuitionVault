from django.contrib import admin
from .models import TuitionPost, TuitionApplication

class TuitionApplicationInline(admin.TabularInline):
    model = TuitionApplication
    extra = 0
    fields = ('user', 'applied_at', 'is_approved')
    readonly_fields = ('user', 'applied_at')

class TuitionPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'class_name', 'location', 'availability')  # Fields to display
    search_fields = ('title', 'class_name', 'location')  # Searchable fields
    list_filter = ('group', 'availability')  # Filters for sidebar
    inlines = [TuitionApplicationInline]

admin.site.register(TuitionPost, TuitionPostAdmin)
