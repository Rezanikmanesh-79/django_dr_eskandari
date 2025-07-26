from django.shortcuts import render ,get_object_or_404
from django.http import HttpResponse
from blog.models import Post


def index(request):
    return HttpResponse("hello ")

def post_list(request):
    posts = Post.published.all()
    context={'posts':posts}
    return render(request, template_name='blog/post-list.html', context=context)

def post_detail(request, pk):
    # try:
    #     post=Post.published.get(pk=pk)
    #     context = {"post":post}
    #     return render(request, template_name='blog/post-detail.html', context=context)
    # except:
    #     return HttpResponse('post dose not exist')
    
    post=get_object_or_404(Post, pk=pk)
    context = {"post":post}
    return render(request, template_name='blog/post-detail.html', context=context)