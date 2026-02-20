from django.contrib import admin
from .models import Theme, Post

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'created_at')
    search_fields = ('name', 'author__username')
    list_filter = ('created_at',)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('theme', 'author', 'created_at', 'updated_at')
    search_fields = ('theme__name', 'author__username', 'content')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')