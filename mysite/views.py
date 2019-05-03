import datetime
from django.shortcuts import render
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from blog.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from django.db.models import Sum
from django.core.cache import cache


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gt=date).values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return blogs[:7]


def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums, dates = get_seven_days_read_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    hot_blog_for_7_days = cache.get('hot_blog_for_7_days')
    if hot_blog_for_7_days is None:
        hot_blog_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blog_for_7_days', hot_blog_for_7_days, 3600)

    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_dat'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_dat'] = get_yesterday_hot_data(blog_content_type)
    context['hot_blog_for_7_days'] = hot_blog_for_7_days
    return render(request, 'home.html', context)
