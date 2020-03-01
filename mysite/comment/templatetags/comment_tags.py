from django import template
from ..models import Comment
from ..forms import CommentForm
from django.contrib.contenttypes.models import ContentType

register = template.Library()


# 获取评论数量
@register.simple_tag
def get_commment_count(obj):
    content_type = ContentType.objects.get_for_model(model=obj)
    comment_count = Comment.objects.filter(content_type=content_type, object_id=obj.id).count()
    return comment_count


# 创建form对象并进行初始化
@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(model=obj)
    content_form = CommentForm(
        initial={"content_type": content_type.model, "object_id": obj.pk, "reply_comment_id": 0})
    return content_form

# 获取查询评论
@register.simple_tag
def get_comments(obj):
    content_type = ContentType.objects.get_for_model(obj)
    conments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None).order_by(
        "-comment_time")
    return conments