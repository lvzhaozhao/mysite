from haystack import indexes
from blog.models import Blog


# 这个文件的作用是设置haystack在生成索引的时候，根据哪些字段来生成索引
# 名字是需要检索的model的名字+Index
class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    # 创建一个字段
    # 每一个索引里必须要有而且只能有一个字段document=True
    text = indexes.CharField(document=True, use_template=True)

    # 给title、content设置索引
    title = indexes.NgramField(model_attr='title')
    content = indexes.NgramField(model_attr='content')

    # 必须重载
    def get_model(self):
        return Blog

    # 重载index_queryset函数
    def index_queryset(self, using=None):
        return self.get_model().objects.order_by('-created_time')
