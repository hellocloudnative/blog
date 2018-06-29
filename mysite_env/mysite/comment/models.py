from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
# Create your models here.
class comment(models.Model):
    content_type=models.ForeignKey(ContentType,verbose_name="类型",on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')
    text=models.TextField(verbose_name="评论内容")
    comment_time=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,related_name="comments", verbose_name="用户",on_delete=models.CASCADE)

    root=models.ForeignKey('self',null=True,related_name="root_comment",on_delete=models.CASCADE)
    parent=models.ForeignKey('self',null=True,related_name="parent_comment",on_delete=models.CASCADE)
    reply_to=models.ForeignKey(User,related_name="replies",null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.text
    class Meta:
        ordering=["comment_time"]
        verbose_name = "评论"
        verbose_name_plural = "评论"