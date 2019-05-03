from django.db import models
from django.db.models.fields import exceptions
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNum, ReadDetail
# Create your models here.


class BlogType(models.Model):
    """博客类型"""
    type_name = models.CharField(max_length=30, verbose_name='分类')

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    """博客详情页"""
    title = models.CharField(max_length=50, verbose_name='标题')
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE, verbose_name='分类')
    content = RichTextUploadingField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    read_details = GenericRelation(ReadDetail, verbose_name='阅读量')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    # 在后台显示阅读量的方法
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(Blog)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.id)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_id': self.id})

    def get_email(self):
        return self.author.email

    def __str__(self):
        return "<Blog: %s>"% self.title

    class Meta:
        ordering = ['-created_time']


