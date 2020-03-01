from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


# 登陆form模型
class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="用户名",
                                        widget=forms.TextInput(
                                            attrs={"class": "form-control", "placeholder": "请输入用户名或邮箱"}))
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码"}))

    # 使用form框架创建完对象调用is_valid()时候，会调用form自定义模型中定于的clean函数
    def clean(self):
        username_or_email = self.cleaned_data["username_or_email"]
        password = self.cleaned_data["password"]
        user = auth.authenticate(username=username_or_email, password=password)
        print("username_or_email:", username_or_email)
        print("password:", password)
        print("user:", user)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data["user"] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码不正确')

        else:
            self.cleaned_data["user"] = user

        return self.cleaned_data


# 注册模型
class RegForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=30,
                               widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入用户名"}))
    email = forms.EmailField(label="邮箱",
                             widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "请输入邮箱"}))
    verification_code = forms.CharField(label="验证码", empty_value=True,
                                        widget=forms.TextInput(
                                            attrs={"class": "form-control", "placeholder": "点击'发送验证码'到邮箱"}))
    password = forms.CharField(label="密码", min_length=3,
                               widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码"}))
    password_again = forms.CharField(label="密码", min_length=6,
                                     widget=forms.PasswordInput(
                                         attrs={"class": "form-control", "placeholder": "请在输入一次"}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            print("request:")
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 验证验证码
        verification_code = self.cleaned_data.get("verification_code", "")
        code = self.request.session.get('register_email_code', '')
        if code == verification_code:
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已存在")
        return email

    def clean_password_again(self):
        password = self.cleaned_data["password"]
        password_again = self.cleaned_data["password_again"]
        if not password == password_again:
            raise forms.ValidationError("两次密码不一致")
        return password_again

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get("verification_code", "")
        print("verification_code:", verification_code)
        if verification_code == "":
            raise forms.ValidationError("验证码不能为空")
        return self.cleaned_data


# 更改昵称
class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(label="新昵称", max_length=20,
                                   widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入新的昵称"}))

    def __init__(self, *args, **kwargs):
        if "user" in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登陆
        if self.user.is_authenticated:
            self.cleaned_data["user"] = self.user
        else:
            raise forms.ValidationError("用户未登陆")
        return self.cleaned_data

    def clean_nickname_new(self):
        nickname = self.cleaned_data.get("nickname_new", None).strip()
        if not nickname:
            raise forms.ValidationError("新昵称不能未空")
        return nickname


# 绑定邮箱
class BindEmailForm(forms.Form):
    email = forms.EmailField(label="邮箱",
                             widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "请输入正确的邮箱"}))

    verification_code = forms.CharField(label="验证码", empty_value=True,
                                        widget=forms.TextInput(
                                            attrs={"class": "form-control", "placeholder": "点击'发送验证码'到邮箱"}))

    def __init__(self, *args, **kwargs):
        if "request" in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登陆
        if self.request.user.is_authenticated:
            self.cleaned_data["user"] = self.request.user
        else:
            raise forms.ValidationError("用户未登陆")

        # 判断用户是否绑定邮箱
        if not self.request.user.email == "":
            raise forms.ValidationError("已经绑定邮箱了")

        verification_code = self.cleaned_data.get("verification_code", "")
        code = self.request.session.get('bind_email_code', '')
        if code == verification_code:
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get("verification_code", "")
        print("verification_code:", )
        if verification_code == "":
            raise forms.ValidationError("邮箱不能为空")
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data["email"]
        print("eamil_cleand_data:", email)
        self.cleaned_data["email2"] = email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("该邮箱已注册")
        return self.cleaned_data

# 修改密码
class Change_password(forms.Form):
    old_password = forms.CharField(label="旧密码", min_length=3,
                                   widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输旧入密码"}))
    new_password = forms.CharField(label="密码", min_length=3,
                                   widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入新密码"}))
    new_password_again = forms.CharField(label="密码", min_length=3,
                                         widget=forms.PasswordInput(
                                             attrs={"class": "form-control", "placeholder": "请在输入一次新密码"}))

    def __init__(self, *args, **kwargs):
        if "request" in kwargs:
            self.request = kwargs.pop('request')
        super(Change_password, self).__init__(*args, **kwargs)

    def clean(self):
        new_password = self.cleaned_data["new_password"]
        new_password_again = self.cleaned_data["new_password_again"]
        if not new_password_again == "" and not new_password_again == new_password:
            raise forms.ValidationError("两次输入的密码不一致")
        return self.cleaned_data

    def clean_old_password(self):
        # 验证
        old_password = self.cleaned_data.get("old_password", "")
        if not self.request.user.check_password(old_password):
            raise forms.ValidationError("旧密码不正确")
        return old_password

# 忘记密码，邮箱验证
class Forget_password(forms.forms.Form):
    username = forms.CharField(label="用户名", max_length=30,
                              widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入用户名"}))
    email = forms.EmailField(label="邮箱",
                             widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "请输入绑定过的邮箱"}))
    verification_code = forms.CharField(label="验证码", empty_value=True,
                                        widget=forms.TextInput(
                                            attrs={"class": "form-control", "placeholder": "点击'发送验证码'到邮箱"}))
    new_password = forms.CharField(label="密码", min_length=3,
                               widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入新密码"}))

    def __init__(self, *args, **kwargs):
        if "request" in kwargs:
            self.request = kwargs.pop('request')
        super(Forget_password, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户不存在")
        return username

    def clean_verification_code(self):
        code = self.request.session.get('forget_password_code', '')
        verification_code = self.cleaned_data.get("verification_code", "")
        if code == verification_code:
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data["email"]
        print("eamil_cleand_data:", email)
        self.cleaned_data["email2"] = email
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱不存在")
        return self.cleaned_data