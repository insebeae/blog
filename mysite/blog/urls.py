from django.urls import path
from . import views
app_name= "blog"
urlpatterns = [
    path("", views.index, name="blog_list"),
    path("detail/<int:blog_id>", views.blog_detail, name="blog_detail"),
    path("detail_type/<int:blog_type_id>", views.detail_type, name="detail_type"),
    path("detail_date/<int:year>/<int:month>", views.detail_date, name="detail_date"),
]
