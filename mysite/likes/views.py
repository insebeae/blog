from django.shortcuts import render
from django.http.response import JsonResponse
from .models import LikeRecord, LikeCount
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
def ErrorResponse(message):
    data = {}
    data["status"] = "Error"
    data["message"] = message
    return JsonResponse(data)

def SuccessResponse(like_num):
    data = {}
    data["status"] = "SUCCESS"
    data["like_num"] = like_num
    return JsonResponse(data)

# Create your views here.
def like_change(request):
    print(":request.user:",request.user)
    if not request.user.id:
        return ErrorResponse("用户登陆异常")
    if not  request.user.is_authenticated:
        return ErrorResponse("用户登陆异常")
    # 获取数据
    content_type = request.GET.get("content_type")
    # content_type = ContentType.objects.get(model=content_type)
    object_id = request.GET.get("object_id")
    is_like = request.GET.get("is_like")
    user = request.user
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        print("ObjectDoesNotExist")
        return ErrorResponse("该博客不存在")
    print("is_like111111:",is_like)
    # 处理数据
    if is_like == "true":
        print("要点赞")
        # 点赞
        likerecord, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id,
                                                               usr=user)
        print("created:",created)
        if created:
            # 未点赞
            likecount, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            likecount.like_num += 1
            likecount.save()
            return SuccessResponse(likecount.like_num)
        else:
            # 已经点赞
            return ErrorResponse("已经点赞")
    else:
        print("取消点赞")
        # 取消点赞
        likerecord = LikeRecord.objects.filter(content_type=content_type, object_id=object_id, usr=user)
        likerecord.delete()
        # 点赞总数减一
        likecount, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
        print("created:",created)
        likecount.like_num -= 1
        likecount.save()
        return SuccessResponse(likecount.like_num)
