import datetime
from django.core.paginator import Paginator
from django.db.models import Count
from blog.models import Blog, BlogType
from read_statistics.models import ReadNum, ReadDetail
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum


def get_seven_days_read_data(content_type):
    """获取前七日的阅读量和日期"""
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        # aggregate 聚合函数 用于计算
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return read_nums, dates


def get_blog_list_connon_date(request, blogs):
    """对博客分页和日期归档"""
    context = {}
    # 每4篇进行分页
    paginator = Paginator(blogs, settings.EACH_PAGE_BLOGS_NUMBER)
    # 获取页码参数（GET请求）
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    # 获取当前页码前后个两页的范围
    currentr_page_num = page_of_blogs.number
    # paginator.num_pages总页数
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + list(
        range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码
    if page_range[0] - 1 >= 2:
        page_range.insert(0, "…")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("…")

    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取博客分类的对应博客数量
    # blog_types = BlogType.objects.all()
    # blog_types_list = []
    # for blog_type in blog_types:
    #     blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
    #     blog_types_list.append(blog_type)
    # context['blog_types'] = blog_types_list
    # annotate注释
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))

    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blog_dates'] = blog_dates_dict
    return context


def get_today_hot_data(content_type):
    """今天热门博客"""
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7]


def get_yesterday_hot_data(content_type):
    """昨天热门博客"""
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:7]
