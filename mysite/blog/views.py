from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Blog, Blog_type
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from read_statistics.utils import get_read_num_once
from user.forms import LoginForm

per_page_blog_num = 7


def get_blog_common_data(request, blog_list):
    # 获取页码参数，get请求
    page_num = request.GET.get("page", 1)
    blog_all_num = blog_list.count()
    blog_type_list = Blog_type.objects.all()
    paginator_blog = Paginator(blog_list, per_page_blog_num)
    blog_list_temp = paginator_blog.get_page(int(page_num))
    blog_list = blog_list_temp.object_list
    page_range = [i for i in range(max(int(page_num) - 2, 1), min(int(page_num) + 2, paginator_blog.num_pages) + 1)]
    # 省略号标签添加
    if page_range[0] - 1 >= 2:
        page_range.insert(1, "...")
    if paginator_blog.num_pages - page_range[-1] >= 2:
        page_range.insert(-1, "...")
    # 首尾页添加
    if not page_range[0] == 1:
        page_range.insert(0, 1)
    if not page_range[-1] == paginator_blog.num_pages:
        page_range.append(paginator_blog.num_pages)

    # 获取博客分类对应的数量
    # 方法一：
    # for blog_type in blog_type_list:
    # blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
    # 方法二
    blog_type_list = Blog_type.objects.annotate(blog_count=Count("blog"))
    # 获取博客日期对应的数量
    context_date = {}
    blog_date_list = Blog.objects.dates("c_time", "month", "DESC")
    for blog_date in blog_date_list:
        context_date[blog_date] = Blog.objects.filter(c_time__year=blog_date.year,
                                                      c_time__month=blog_date.month).count()
    print(context_date)
    return blog_all_num, blog_type_list, paginator_blog, blog_list_temp, blog_list, page_range, context_date


# Create your views here.
def index(request):
    print("request.user:",request.user)
    print("request.user:",request.user.id)
    if not request.user.id:
        print("request.user.id")
    blog_list = Blog.objects.filter(is_deleted=False).order_by("-c_time", "title", "m_time")
    blog_all_num, blog_type_list, paginator_blog, blog_list_temp, blog_list, page_range, context_date = get_blog_common_data(
        request,
        blog_list)
    print("context_date:", context_date)

    return render(request, "blog/blog_list.html", locals())


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    # 获取key，设置cookie
    key = get_read_num_once(request, blog)
    # 上篇博客
    previous_blog = Blog.objects.filter(c_time__gt=blog.c_time)
    previous_blog = previous_blog.last()
    # 下篇博客
    next_blog = Blog.objects.filter(c_time__lt=blog.c_time)
    next_blog = next_blog.first()

    # 创建form对象并进行初始化
    login_form = LoginForm()
    response = render(request, "blog/detail.html", locals())

    response.set_cookie(key, True)
    return response


def detail_type(request, blog_type_id):
    # 获取页码参数，get请求
    page_num = request.GET.get("page", 1)
    blog_type = get_object_or_404(Blog_type, id=blog_type_id)
    blog_list = Blog.objects.filter(blog_type=blog_type)
    blog_all_num, blog_type_list, paginator_blog, blog_list_temp, blog_list, page_range, context_date = get_blog_common_data(
        request,
        blog_list)

    return render(request, "blog/blog_detail_type.html", locals())


def detail_date(request, year, month):
    # 获取页码参数，get请求
    page_num = request.GET.get("page", 1)
    blog_list = Blog.objects.filter(c_time__year=year, c_time__month=month)
    blog_all_num, blog_type_list, paginator_blog, blog_list_temp, blog_list, page_range, context_date = get_blog_common_data(
        request,
        blog_list)
    blog_date_list = Blog.objects.dates("c_time", "month", "DESC")
    return render(request, "blog/blog_detail_date.html", locals())

