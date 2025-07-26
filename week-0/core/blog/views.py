from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post


def index(request):
    return HttpResponse("hello ")

def post_list(request):
    posts = Post.published.all()
    context={'posts':posts}
    return render(request, template_name='blog/post-list.html', context=context)
def post_detail(request, pk):
    post=Post.published.get(pk=pk)
    context = {"post":post}
    return render(request, template_name='blog/post-detail.html', context=context)
