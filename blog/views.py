from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog, BlogType
from blog.utils import get_blog_list_connon_date
from read_statistics.models import ReadNum, ReadDetail
from django.utils import timezone

# Create your views here.


def blog_detail(request, blog_id):
    """博客页面"""
    # get_list_or_404() 获取博客的详细信息
    blog = get_object_or_404(Blog, id=blog_id)
    ct = ContentType.objects.get_for_model(Blog)
    # 每次查看博客内容阅读量+1
    if not request.COOKIES.get('blog_%s_read'% blog_id):
        # 总阅读量+1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=blog.id)
        readnum.read_num += 1
        readnum.save()
        # 当天阅读量+1
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=blog.id, date=date)
        readDetail.read_num += 1
        readDetail.save()

    context = {}
    context['blog'] = blog
    # 获取上一条博客
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    # 获取下一条博客
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()

    # 响应
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie('blog_%s_read' % blog_id, 'true')
    return response


def blog_list(request):
    """返回博客的列表"""
    blogs = Blog.objects.all()
    context = get_blog_list_connon_date(request, blogs)
    return render(request, 'blog/blog_list.html', context)


def blogs_with_type(request, blog_type_id):
    """分类页面"""
    context = {}
    blog_type = get_object_or_404(BlogType, id=blog_type_id)
    blogs = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    context = get_blog_list_connon_date(request, blogs)
    return render(request, 'blog/blog_with_type.html', context)


def blog_with_date(request, year, month):
    context = {}
    blogs = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context['blog_with_date'] = '%s年%s月' % (year, month)
    context = get_blog_list_connon_date(request, blogs)
    return render(request, 'blog/blog_with_date.html', context)
