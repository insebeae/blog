from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm, RegForm, ChangeNicknameForm, BindEmailForm,Change_password,Forget_password
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from .models import Profile
from mysite.settings_base import EMAIL_HOST_USER
import hashlib, datetime


# Create your views here.
# 登陆
def login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data["user"]
            auth.login(request, user)
            return redirect(request.GET.get("from", reverse("home")))
        return render(request, "user/login.html", locals())
    else:
        login_form = LoginForm()
    return render(request, "user/login.html", locals())


# 模态框登陆验证
def login_for_modal(request):
    print("login_for_modal")
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data["user"]
        auth.login(request, user)
        data["status"] = "SUCCESS"
    else:
        data["status"] = "ERROE"
    print("data:", data)
    return JsonResponse(data)


# 注册用户
def register(request):
    print('request.GET.get("from", reverse("home")):', request.GET.get("from", reverse("home")))
    if request.method == "POST":
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data["username"]
            password = reg_form.cleaned_data["password"]
            email = reg_form.cleaned_data["email"]
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 删除session
            del request.session["register_email_code"]
            # 登陆用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get("from", reverse("home")))
    else:
        reg_form = RegForm()
    return render(request, "user/register.html", locals())


# 等出
def logout(request):
    auth.logout(request)
    from_url = request.GET.get("from")
    if "user_info" in from_url:
        return redirect(reverse("home"))
    return redirect(request.GET.get("from"))


def user_info(request):
    return render(request, "user/user_info.html", locals())


# 修改昵称
def change_nickname(request):
    redirect_to = request.GET.get("from", reverse("home"))
    if request.method == "POST":
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data["nickname_new"]
            profile, new = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)

    else:
        form = ChangeNicknameForm()
    context = {}
    context["form"] = form
    context["page_title"] = "修改昵称"
    context["form_title"] = "修改昵称"
    context["sub_text"] = "提交修改"
    context["redirect_back"] = redirect_to
    return render(request, "form.html", context)


# 绑定邮箱
def bingd_email(request):
    redirect_to = request.GET.get("from", reverse("home"))
    if request.method == "POST":
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data["email"]
            email2 = form.cleaned_data["email2"]
            print("email:",email)
            print("email2:",email2)
            request.user.email = email2
            request.user.save()
            # 删除session
            del request.session["send_email_code"]
            return redirect(redirect_to)
    else:
        form = BindEmailForm()
    context = {}
    context["form"] = form
    context["page_title"] = "绑定邮箱"
    context["form_title"] = "绑定邮箱1"
    context["sub_text"] = "绑定"
    context["redirect_back"] = redirect_to
    return render(request, "form_email.html", context)

# 更改密码
def change_password(request):
    redirect_to = reverse("home")
    if request.method == "POST":
        form = Change_password(request.POST, request=request)
        if form.is_valid():
            user= request.user
            new_password = form.cleaned_data["new_password"]
            user.set_password(new_password)
            request.user.save()
            logout(request)
            return redirect(reverse("home"))
    else:
        form = Change_password()
    context = {}
    context["form"] = form
    context["page_title"] = "修改密码"
    context["form_title"] = "修改密码"
    context["sub_text"] = "修改"
    context["redirect_back"] = redirect_to
    return render(request, "form.html", context)
def hash_code(value, alt="mysite"):
    h = hashlib.sha256()
    value += alt
    h.update(value.encode())
    return h.hexdigest()


def send_code(request):
    # print("email:", email)
    send_for = request.GET.get("send_for","")
    print("send_for:",send_for)
    email = request.GET.get("email")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(email, now)
    data = {}
    print("email:", email)
    if not email == "":
        from django.core.mail import EmailMultiAlternatives

        subject = '来自个人博客的注册确认邮件'
        print("发送成功")
        print("email:", email)
        text_content = '''感谢把绑定邮箱，如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
        html_content = '''<p>感谢绑定</p>你的验证码为{}" '''.format(code)
        msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        request.session[send_for] = code
        data["status"] = "SUCCESS"
        return JsonResponse(data)
    else:
        data["status"] = "ERROR"
        return JsonResponse(data)


# 忘记密码
def forget_password(request):
    redirect_to = reverse("home")
    if request.method == "POST":
        form = Forget_password(request.POST, request=request)
        if form.is_valid():
            username = form.cleaned_data["username"]
            new_password = form.cleaned_data["new_password"]
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect(redirect_to)
    else:
        form = Forget_password()
    context = {}
    context["form"] = form
    context["page_title"] = "忘记密码"
    context["form_title"] = "忘记密码"
    context["sub_text"] = "修改"
    context["redirect_back"] = redirect_to
    return render(request, "forget_password.html", context)