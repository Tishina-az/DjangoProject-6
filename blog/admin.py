from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'preview', 'publication_at',)
    list_filter = ('created_at',)
    search_fields = ('title', 'content',)
