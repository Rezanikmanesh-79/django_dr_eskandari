from django.shortcuts import render ,get_object_or_404 ,redirect
from django.http import HttpResponse
from blog.models import Post,Ticket,Comment
import datetime
from django.core.paginator import Paginator , EmptyPage ,PageNotAnInteger
from blog.forms import TicketForm,CommentForm,PostForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
def index(request):
    # we dont need this anymore cuz we in templatetags/blog_tags.py made custom templatetags and our server just need calculate once
    # posts=Post.published.all()
    # comment=Comment
    # context={"posts":posts,"comments":comment}
    return render (request,template_name='blog/index.html')

def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, per_page=2)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    # if user input some ting is not int
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {'posts': page_obj}
    return render(request, 'blog/post-list.html', context)
def post_detail(request, pk):
    # try:
    #     post=Post.published.get(pk=pk)
    #     context = {"post":post}
    #     return render(request, template_name='blog/post-detail.html', context=context)
    # except:
    #     return HttpResponse('post dose not exist')
    
    post = get_object_or_404(Post, pk=pk, status=Post.Status.PUBLISHED)
    comment=post.comment.filter(is_active=True)
    form=CommentForm()
    context = {"post":post,"form":form,'comment':comment}
    return render(request, template_name='blog/post-detail.html', context=context)

def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(
                message=cd['message'],
                name=cd['name'],
                email=cd['email'],
                phone=cd['phone'],
                subject=cd['subject']
            )
            return redirect('blog:index')
    else:
        form = TicketForm()

    return render(request, 'forms/ticket.html', {'form': form})
# we only access this with post cuz of "require_POST"
@require_POST
def post_comment(request,pk):
    post=get_object_or_404(Post,pk=pk,status=Post.Status.PUBLISHED)
    comment=None
    form = CommentForm(request.POST)
    if form.is_valid():
# "commit=False" is mean create obj but dont save in database 
        comment=form.save(commit=False)
        comment.post=post
        comment.save()
    context={'post':post,'comment':comment,'form':form}
    return render(request,template_name='forms/comment.html',context=context)

@login_required
def create_post_view(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # every time we want to use ForeignKey we should do it in this way
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:post-list")  
    else:
        form = PostForm()

    return render(request, "forms/post.html", {"form": form})

def post_search(request):
    pass