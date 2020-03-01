from django.urls import path
from . import views
app_name = "user"
urlpatterns = [
    path('login/', views.login, name="login"),
    path('login_for_modal/', views.login_for_modal, name="login_for_modal"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),
    path('user_info/', views.user_info, name="user_info"),
    path('change_nickname/', views.change_nickname, name="change_nickname"),
    path('bingd_email/', views.bingd_email, name="bingd_email"),
    path('change_password/', views.change_password, name="change_password"),
    path('forget_password/', views.forget_password, name="forget_password"),
    path('send_code/', views.send_code, name="send_code"),
]