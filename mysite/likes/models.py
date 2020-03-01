from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
# Create your models here.
# 点赞
class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    # 这是具体的一个类的实例
    content_object = GenericForeignKey('content_type', 'object_id')

    like_num = models.IntegerField(default=0)

# 点赞详细
class LikeRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    # 这是具体的一个类的实例
    content_object = GenericForeignKey('content_type', 'object_id')

    usr = models.ForeignKey(User, on_delete=models.CASCADE)
    like_time = models.DateField(auto_now_add=True)