from django.contrib import admin
from .models import LikeCount,LikeRecord
# Register your models here.
#
@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display=('content_object','liked_num')
@admin.register(LikeRecord)
class LikeCountAdmin(admin.ModelAdmin):
    list_display=('content_type','user','liked_time')