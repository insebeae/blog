from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from mysite.utils import send_mail
import threading
# render_to_string渲染模板并返回str类型，两个参数，第一个为模板路径，第二个要渲染的内容
from django.template.loader import render_to_string

# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    # 这是具体的一个类的实例
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateField(auto_now_add=True)
    usr = models.ForeignKey(User, on_delete=models.CASCADE)

    # 该回复的最顶级评论
    root = models.ForeignKey("self", related_name="root_comment", null=True, on_delete=models.CASCADE)
    # 上级回复(上次回复的对象的实例)
    parent = models.ForeignKey("self", related_name="parent_comment", null=True, on_delete=models.CASCADE)
    # 回复人
    reply_to = models.ForeignKey(User, related_name="reply_comment", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-comment_time"]
        verbose_name = "评论"
        verbose_name_plural = "评论"

    def send_mail(self):
        email = self.content_object.author.email
        text_content = "有人进行评论" + self.text + "\n" + self.content_object.get_url()
        url = "http://127.0.0.1:8000" + self.content_object.get_url()
        text_content = render_to_string("comment/base_email.html",locals())
        if not email == "":

            send_mail = SendMail(text_content, email)
            send_mail.start()


class SendMail(threading.Thread):
    def __init__(self, text_content, email):
        self.text_content = text_content
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.text_content, self.email)
