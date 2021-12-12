from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from blog.templatetags import extrass
# Create your views here.
from .models import Post, Comments


def Bloghome(request):
    Allpost = Post.objects.all()
    context = {'Allpost': Allpost}
    return render(request, 'blog/Bloghome.html', context)


def Blogpost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = Comments.objects.filter(post=post, parent=None)
    post.views = post.views + 1
    post.save()
    replies = Comments.objects.filter(post=post).exclude(parent=None)
    reDict = {}
    for reply in replies:
        if reply.parent.sno not in reDict.keys():
            reDict[reply.parent.sno] = [reply]
        else:
            reDict[reply.parent.sno].append(reply)
    print(reDict)
    context = {'post': post, 'comments': comments, 'reDict': reDict}
    return render(request, 'blog/Blogpost.html', context)


def Blogcomment(request):
    if request.method == "POST":
        print(request.POST)
        comment = request.POST.get("comment")
        user = request.user
        id = request.POST.get('postsrn')
        try:
            post = Post.objects.filter(srn=id).get()
        except ValueError:
            return JsonResponse({
                "status": False,
                "message": "post doesnot exisst"
            })
        commentsrn = request.POST.get('parentsrn')
        if commentsrn == "":
            comments = Comments(comment=comment, post=post, user=user)
            comments.save()
            messages.success(request, 'Comment has been added.')
        else:
            parant = Comments.objects.get(sno=commentsrn)
            comments = Comments(comment=comment, post=post, user=user, parent=parant)
            comments.save()
            messages.success(request, 'Replyy has been added.')
        return redirect(f'/blog/{post.slug}')
    return JsonResponse({'status': False, 'massage': "invallid request"})
