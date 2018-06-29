from django.contrib import admin
from .models import Blog, BlogType

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "type_name")

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display =("id","title", "content", "author","get_read_num", "create_time", "last_time")

# @admin.register(ReadNum)
# class ReadNumAdmin(admin.ModelAdmin):
#     list_display =('read_num','blog')

        
    
