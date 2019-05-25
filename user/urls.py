from django.urls import path
from .views import login, register, login_for_medal, logout, user_info, change_nickname, bind_email, change_password, send_verification_code, forgot_password


urlpatterns = [
    path('login/', login, name='login'),
    path('login_for_medal/', login_for_medal, name='login_for_medal'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('user_info/', user_info, name='user_info'),
    path('change_nickname/', change_nickname, name='change_nickname'),
    path('bind_email/', bind_email, name='bind_email'),
    path('send_verification_code/', send_verification_code, name='send_verification_code'),
    path('change_password/', change_password, name='change_password'),
    path('forgot_password/', forgot_password, name='forgot_password'),
]


