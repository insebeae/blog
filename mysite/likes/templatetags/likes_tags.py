from django import template
from ..models import LikeCount, LikeRecord
from django.contrib.contenttypes.models import ContentType

register = template.Library()


# 获取评论数量
@register.simple_tag
def get_likes_count(obj):
    print("obj:",obj)
    content_type = ContentType.objects.get_for_model(model=obj)
    like_count = LikeCount.objects.filter(content_type=content_type, object_id=obj.id)
    if like_count:
        like_count = LikeCount.objects.get(content_type=content_type, object_id=obj.id).like_num
    else:
        like_count = 0
    print("like_count：", like_count)
    return like_count


# 获取点赞状态
@register.simple_tag(takes_context=True)
def get_likes_status(context, obj):
    content_type = ContentType.objects.get_for_model(model=obj)
    if not context['user'].id:
        return ""
    if context['user'] is None:
        return ""
    if context['user'] =="AnonymousUser":
        return ""
    if LikeRecord.objects.filter(content_type=content_type, object_id=obj.id, usr=context['user']).exists():
        return "active"
    else:
        return ""

# 获取contenttype
@register.simple_tag
def get_content_type_obj(obj):
    content_type = ContentType.objects.get_for_model(model=obj)
    return content_type