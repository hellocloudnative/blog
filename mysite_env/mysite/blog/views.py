from django.shortcuts import render,get_object_or_404
from .models import Blog,BlogType
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from read_statistics.utils import read_statistics_once_read
from comment.models import comment
from django.contrib.contenttypes.models import ContentType
from comment.forms import CommentForm
import markdown
from django.views import  view

def get_blog_list_common_data(request,blogs_all_list):
    paginator=Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER)#每十篇进行分页
    page_num=request.GET.get('page',1) #获取url页码参数（GET请求）
    page_of_blogs=paginator.get_page(page_num)
    currentr_page_num=page_of_blogs.number #获取当前页码
    page_range= list(range(max(currentr_page_num-2,1),currentr_page_num))+\
                list(range(currentr_page_num,min(currentr_page_num+2,paginator.num_pages) +1))
    #加上省略页码标记
    if page_range[0]-1>2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1]>2:
        page_range.append('...')
    #加上首页尾页
    if page_range[0] !=1:
        page_range.insert(0,1)
    if page_range[-1] !=paginator.num_pages:
        page_range.append(paginator.num_pages)
    #获得日期归档对应的博客数量
    blog_dates= Blog.objects.dates('create_time','month',order="DESC")

    blog_dates_dict={}
    for blog_date in blog_dates:
        blog_count=Blog.objects.filter(create_time__year=blog_date.year,create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date]=blog_count

    #获取博客分类的对应博客数量
    # blog_types = BlogType.objects.all()
    # blog_type_list=[]
    # for blog_type in blog_types:
    #     blog_type.blog_count=Blog.objects.filter(blog_type=blog_type).count()
    #     blog_type_list.append(blog_type)
    context={}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs']=page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return context


def  blog_list(request):
    blogs_all_list=Blog.objects.all()  

    context=get_blog_list_common_data(request,blogs_all_list)
    return render(request, "blog/blog_list.html", context)


def blogs_with_type(request,blog_type_pk):
    blog_type=get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list=Blog.objects.filter(blog_type=blog_type) 

    context=get_blog_list_common_data(request,blogs_all_list)
    context['blog_type']=blog_type
    return render(request,"blog/blogs_with_type.html",context)


def blogs_with_date(request,year,month):
    blogs_all_list=Blog.objects.filter(create_time__year=year, create_time__month=month)  

    context=get_blog_list_common_data(request,blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' %(year,month)
    return render(request,"blog/blogs_with_date.html",context)


def blog_detail(request,blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key =read_statistics_once_read(request,blog)
    blog_content_type=ContentType.objects.get_for_model(Blog)
    comments=comment.objects.filter(content_type=blog_content_type,object_id=blog.pk,parent=None)
    # if not request.COOKIES.get('blog_%s_readed' % blog_pk):
    #     ct=ContentType.objects.get_for_model(Blog)

    #     if ReadNum.objects.get(content_type=ct,object_id=self.pk).count():
    #         #存在记录
    #         readnum =ReadNum.objects.get(content_type=ct,object_id=self.pk)
    #     else:
    #         #不存在记录
    #         readnum =ReadNum(content_type=ct,object_id=self.pk)
    #     readnum.read_num +=1
    #     readnum.save()  
        # if ReadNum.objects.filter(blog=blog).count():
        #     #存在记录
        #     readnum = ReadNum.objects.get(blog=blog)
        # else:
        #     #不存在对应记录
        #     readnum=ReadNum(blog=blog)
        # #计数+1
        # readnum.read_num +=1
        # readnum.save()  


    context = {}
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    context['blog']=blog
    blog.content=markdown.markdown(blog.content,['extra','codehilite','toc',])

    context['user']=request.user
    # context['comments']=comments.order_by('-comment_time')
    # context['comment_count']= comments=comment.objects.filter(content_type=blog_content_type,object_id=blog.pk).count()
    # context['comment_form']=CommentForm(initial={"content_type":blog_content_type.model,'object_id':blog_pk,'reply_comment_id':0})
    response = render(request, "blog/blog_detail.html", context)
    response.set_cookie(read_cookie_key,'true')
    return response