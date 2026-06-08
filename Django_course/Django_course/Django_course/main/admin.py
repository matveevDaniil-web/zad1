#from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import News, Comment

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date')
    list_filter = ('pub_date', 'author')
    search_fields = ('title', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'created_at')
    list_filter = ('created_at', 'user')