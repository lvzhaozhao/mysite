from django.urls import path
from likes.views import like_change

name = 'comment'
urlpatterns = [
    path('like_change/', like_change, name='like_change'),
]
