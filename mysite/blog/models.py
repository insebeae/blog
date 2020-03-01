from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod
from django.contrib.contenttypes.fields import GenericRelation
from read_statistics.models import ReadDetail
from django.urls import reverse


# Create your models here.
# 博客类型
class Blog_type(models.Model):
    type_name = models.CharField(max_length=15, verbose_name="类型名")
    type_describtion = models.CharField(max_length=200, verbose_name="类型描述")
    type_num = models.IntegerField(default=0, null=True, blank=True, verbose_name="类型号")

    def __str__(self):
        return self.type_name

    class Meta:
        # ordering = ["-c_time"]
        verbose_name = "博客类型"
        verbose_name_plural = "博客类型"


# 博客
class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=30, verbose_name="标题")
    blog_type = models.ForeignKey(Blog_type, on_delete=models.DO_NOTHING, verbose_name="博客类型")
    content = RichTextUploadingField(verbose_name="内容")
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    m_time = models.DateTimeField(auto_now=True, verbose_name="最新修改时间")
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1, verbose_name="作者")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    read_details = GenericRelation(ReadDetail)

    def get_url(self):
        return reverse("blog:blog_detail", kwargs={"blog_id": self.id})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-c_time", "title", "m_time"]
        verbose_name = "博客"
        verbose_name_plural = "博客"

# # 博客数量
# class ReadNum(models.Model):
#     readed_num = models.IntegerField(default=0, verbose_name="阅读数量")
#     blog = models.OneToOneField(Blog, on_delete=models.CASCADE, verbose_name="关联博客")
#
#     class Meta:
#         verbose_name = "阅读数量"
#         verbose_name_plural = "阅读数量"
