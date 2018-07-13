from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod,ReadDetail
from django.contrib.contenttypes.fields import GenericRelation
from mdeditor.fields import MDTextField



class BlogType(models.Model):
    type_name = models.CharField(verbose_name="文章类型",max_length = 15)

    def __str__(self):
        return self.type_name
    class Meta:
        verbose_name="文章类型"
        verbose_name_plural="文章类型"

class Blog(models.Model,ReadNumExpandMethod):
    title = models.CharField(verbose_name="标题",max_length = 50)
    blog_type = models.ForeignKey(BlogType, verbose_name="文章类型",on_delete = models.CASCADE)
    content = MDTextField(verbose_name="文章内容")
    author = models.ForeignKey(User, verbose_name="作者",on_delete = models.CASCADE)
    read_details = GenericRelation(ReadDetail,verbose_name="文章对应阅读数")
    create_time = models.DateTimeField(verbose_name="发表时间",auto_now_add = True)
    last_time = models.DateTimeField(verbose_name="修改时间",auto_now_add = True)

    # def get_read_num(self):
    #     try:
    #         return self.readnum.read_num
    #     except exceptions.ObjectDoesNotExist:
    #         return 0
 

    def __str__(self):
        return "<Blog:　%s＞" % self.title


    class Meta:
        ordering=["-create_time"]
        verbose_name="文章"
        verbose_name_plural="文章"

# class  ReadNum(models.Model):
#         read_num = models.IntegerField(default=0)
#         blog = models.OneToOneField(Blog, on_delete=models.CASCADE)


            
        