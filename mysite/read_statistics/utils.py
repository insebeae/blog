import datetime
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum, ReadDetail
from django.utils import timezone
from django.db.models import Sum
from blog.models import Blog

def get_read_num_once(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "{}_detail_{}".format(ct.model, obj.pk)
    if not request.COOKIES.get(key):
        ct = ContentType.objects.get_for_model(obj)
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        # 总计数加一
        readnum.read_num += 1
        readnum.save()
        # 当前日期计数加一
        date = timezone.now().date()
        readdetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readdetail.read_num += 1
        readdetail.save()

    return key


def get_seven_days_read_date(content_type):
    today = timezone.now().date()
    result_all = []
    date_all = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        date_all.append(date.strftime("%Y/%m/%d"))
        readdetails = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = readdetails.aggregate(read_num_sum=Sum('read_num'))
        # 若result["read_num_sum"]有值则添加，为fALSE则将0设置
        result_all.append(result["read_num_sum"] or 0)

    return result_all, date_all


def get_today_hot_data(content_type):
    today = timezone.now().date()
    # ysetday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today)
    print("read_details:", read_details)
    return read_details[:7]


def get_ysetday_hot_data(content_type):
    today = timezone.now().date()
    ysetday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=ysetday)
    print("read_details:", read_details)
    return read_details[:7]


