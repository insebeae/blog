from .models import Comment
from django.urls import reverse
from .forms import CommentForm
from django.http.response import JsonResponse



# Create your views here.
# 添加评论
def update_comment(request):
    referer = request.META.get("HTTP_REFERER", reverse("home"))
    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():

        parent = comment_form.cleaned_data["parent"]
        if not parent is None:
            root = parent.root if parent.root else parent
            reply_to = parent.usr
            comment = Comment.objects.create(usr=request.user, text=comment_form.cleaned_data["text"],
                                             object_id=comment_form.cleaned_data["object_id"],
                                             content_object=comment_form.cleaned_data["content_object"], parent=parent,
                                             root=root, reply_to=reply_to)
        else:
            comment = Comment.objects.create(usr=request.user, text=comment_form.cleaned_data["text"],
                                             object_id=comment_form.cleaned_data["object_id"],
                                             content_object=comment_form.cleaned_data["content_object"],parent=parent)
        # return redirect(referer)
        data = {}
        data["text"] = comment.text
        data["username"] = comment.usr.get_nickname_or_username()
        data["comment_time"] = comment.comment_time.strftime("%Y/%m/%d")
        data["reply_to"] = parent.usr.get_nickname_or_username() if not parent is None else "-1"
        data["pk"] = comment.pk
        if parent:
            data["root_pk"] = parent.root.pk if not parent.root is None else parent.pk
        else:
            data["root_pk"] = ""
        data["parent_text"] = parent.text if not parent is None else ""
        comment.send_mail()

        return JsonResponse(data)
    else:
        message = comment_form.errors
        # return render(request, "error.html", locals())
        return JsonResponse({"status": message})



