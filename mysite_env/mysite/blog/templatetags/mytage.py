from django import template
import re
from blog.models import Blog
from django.contrib.contenttypes.models import ContentType
from comment.models import  comment
from comment.forms import CommentForm
register = template.Library()

@register.filter
def remove(var):
    if "</div>" in var:
        list1 =re.findall(b'<div style=".*?">(.+)</div>',var,re.I|re.S|re.M)
        result="".join(list1)
        return result
    else:
        return var
@register.simple_tag
def get_comment_count(obj):
    content_type=ContentType.objects.get_for_model(obj)
    return comment.objects.filter(content_type=content_type,object_id=obj.pk).count()
@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form=CommentForm(initial={"content_type": content_type.model, 'object_id': obj.pk, 'reply_comment_id': 0})
    return form

@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-comment_time')

