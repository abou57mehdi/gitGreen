
# Register your models here.
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'table_name')
    search_fields = ('title', 'description')
    list_filter = ('table_name',)
