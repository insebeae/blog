from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    nickname = models.CharField(max_length=20, verbose_name="昵称")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户")

    def __str__(self):
        return "{} :{}".format(self.nickname, self.user.username)

# 定义一个获取昵称的放发并绑定到User类中
def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        return Profile.objects.get(user=self).nickname
    else:
        return self.username

User.get_nickname_or_username = get_nickname_or_username
