from django.contrib import admin
from blog.models import Blog,Blog_type


# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "title",'get_read_num', "c_time", "m_time","author","is_deleted")
    ordering = ("id",)

@admin.register(Blog_type)
class BolgTypeadmin(admin.ModelAdmin):
    list_display = ("id","type_name","type_num")
    ordering = ("id",)

# @admin.register(ReadNum)
# class ReadNumadmin(admin.ModelAdmin):
#     list_display = ("readed_num","blog")
