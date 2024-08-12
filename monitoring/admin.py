from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'table_name', 'image')  # Add image here
    search_fields = ('title', 'description')
    list_filter = ('table_name',)
    fields = ('title', 'description', 'table_name', 'image')  # Ensure image is editable in the form
