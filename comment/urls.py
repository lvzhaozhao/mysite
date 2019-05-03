from django.urls import path
from comment.views import update_comment

name = 'comment'
urlpatterns = [
    path('update_comment/', update_comment, name='update_comment'),
]
