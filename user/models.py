from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='昵称')
    nickname = models.CharField(max_length=20)

    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname, self.user.username)


def get_nickname(user):
    if Profile.objects.filter(user=user).exists():
        profile = Profile.objects.get(user=user)
        return profile.nickname
    else:
        return ''


def has_nickname(user):
    return Profile.objects.filter(user=user).exists()


def get_nickname_or_username(user):
    if Profile.objects.filter(user=user).exists():
        profile = Profile.objects.get(user=user)
        return profile.nickname
    else:
        return user.username


User.get_nickname = get_nickname
User.has_nickname = has_nickname
User.get_nickname_or_username = get_nickname_or_username
