from mysite.settings_base import EMAIL_HOST_USER
def send_mail(text_content, email):

    if not email == "":
        from django.core.mail import EmailMultiAlternatives
        subject = '来自个人博客的评论通知'
        html_content = '''
            <p style="color:red">Python是一种计算机编程语言。，所以，任何一种编程语言都有自己的一套语法，，然后执行。Python也不例外。</p>
        '''
        msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("发送成功")
    else:
        pass