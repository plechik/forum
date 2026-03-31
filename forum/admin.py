from django.contrib import admin
from .models import Thread, Post, Theme

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')
    list_filter = ('created_at',)
@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')
    list_filter = ('created_at',)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'created_at', 'updated_at')
    search_fields = ('thread__name', 'author__username', 'content')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')