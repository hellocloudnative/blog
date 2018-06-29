from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.urls import reverse
from comment.forms import CommentForm
from .models import comment
from django.http import  JsonResponse
from django.contrib import auth
# Create your views here.


def update_comment(request):
    # referer = request.META.get("HTTP_REFERER", reverse("blog_tittle"))
    # #数据检查
    # if not request.user.is_authenticated:
    #     return render(request, 'error.html', {"message": "用户未登录","redirect_to":referer})
    # text=request.POST.get('text','').strip()
    # if text=="":
    #     return render(request,'error.html',{"message":"评论内容为空","redirect_to":referer})
    # try:
    #     content_type=request.POST.get('content_type','')
    #     object_id=int(request.POST.get('object_id','0'))
    #     model_class=ContentType.objects.get(model=content_type).model_class()
    #     model_obj=model_class.objects.get(pk=object_id)
    # except Exception as e:
    #     return render(request, 'error.html', {"message": "评论对象不存在","redirect_to":referer})
    # #检查通过，保存数据
    # Comment=comment()
    # Comment.user=request.user
    # Comment.text=text
    # Comment.content_object=model_obj
    # Comment.save()
    # return  redirect(referer)
    referer=request.META.get('HTTP_REFERER',reverse('blog_list'))
    comment_form=CommentForm(request.POST,user=request.user)
    data = {}
    if comment_form.is_valid():
        #检查通过，保存数据
        Comment=comment()
        Comment.user=comment_form.cleaned_data['user']
        Comment.text=comment_form.cleaned_data['text']
        Comment.content_object=comment_form.cleaned_data['content_object']

        parent=comment_form.cleaned_data['parent']
        if not parent is None:
            Comment.root=parent.root if not parent.root is None else parent
            Comment.parent=parent
            Comment.reply_to = parent.user
        Comment.save()

        #返回数据
        data['status']='SUCCESS'
        data['username']=Comment.user.username
        data['comment_time']=Comment.comment_time.timestamp()
        data['text']=Comment.text
        if not parent is None:
            data['reply_to']=Comment.reply_to.username
        else:
            data['reply_to']=''
        data['pk']=Comment.pk
        data['root_pk']=Comment.root.pk if not Comment.root is None else ''
    else:
        # return render(request, 'error.html', {"message":comment_form.errors , "redirect_to": referer})
        data['status']='ERROR'
        data['message']=list(comment_form.errors.values())[0][0]
    return JsonResponse(data)