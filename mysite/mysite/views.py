from django.shortcuts import render
import datetime
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Sum
from blog.models import Blog
from read_statistics.utils import get_seven_days_read_date, get_today_hot_data, get_ysetday_hot_data


def get_seven_day_hot_data():
    today = timezone.now().date()
    seven_day = today - datetime.timedelta(days=7)
    read_details = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=seven_day) \
        .values("id", "title") \
        .annotate(read_num_sum=Sum("read_details__read_num")) \
        .order_by("-read_num_sum")
    return read_details[:7]


# Create your views here.
def index(request):
    # 获取七天热门博客的缓存数据
    get_seven_day_all = cache.get("get_seven_day_all", 'expired')
    if get_seven_day_all == "expired":
        get_seven_day_all = get_seven_day_hot_data()
        cache.set("get_seven_day_all", get_seven_day_all, 3600)
        print("无缓存")
    else:
        print("有缓存")

    blog_content_type = ContentType.objects.get_for_model(Blog)
    result_all, date_all = get_seven_days_read_date(blog_content_type)
    result_hot_today_all = get_today_hot_data(blog_content_type)
    result_hot_ysetday_all = get_ysetday_hot_data(blog_content_type)
    get_seven_day_all = get_seven_day_hot_data()
    return render(request, "index.html", locals())


