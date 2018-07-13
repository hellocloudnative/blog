from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone
# Create your models here.
 

class ReadNum(models.Model):
    read_num = models.IntegerField(verbose_name="阅读数",default=0)

    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    class Meta:
        verbose_name="阅读数"
        verbose_name_plural="阅读数"
class ReadNumExpandMethod():
    def get_read_num(self):
        ct=ContentType.objects.get_for_model(self)
        try:
            readnum = ReadNum.objects.get(content_type=ct,object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

class ReadDetail(models.Model):
    date=models.DateField(verbose_name="阅读日期",default=timezone.now)
    read_num=models.IntegerField(verbose_name="阅读数",default=0)

    content_type = models.ForeignKey(ContentType,verbose_name="文章",on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')
    class Meta:
        verbose_name="文章对应阅读数"
        verbose_name_plural="文章对应阅读数"