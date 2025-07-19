from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post


def index(request):
    return HttpResponse("hello ")

def post_list(request):
    post = Post.published.all()
    context={'posts':post}
    return render(request, template_name='blog/post-list.html', context=context)
def post_detail(request, pk):
    post=Post.published.filter(pk=pk)
    print(post)
