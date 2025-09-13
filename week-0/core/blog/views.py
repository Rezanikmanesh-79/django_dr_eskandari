from django.shortcuts import render ,get_object_or_404 ,redirect
from django.http import HttpResponse
# my models
from blog.models import Post,Ticket,Comment,Image
import datetime
from django.core.paginator import Paginator , EmptyPage ,PageNotAnInteger
# my forms
from blog.forms import TicketForm,CommentForm,PostForm,SearchForm,LoginForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# this for search postgres
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
# we use django auth system
from django.contrib.auth import login,logout,authenticate


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
        # when we want to add file like image we use (request.FILES)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # every time we want to use ForeignKey we should do it in this way
            post = form.save(commit=False)
            post.author = request.user
            post.save()            
            for i in range(1, 3):  # تعداد فیلدهای تصویر
                image_file = form.cleaned_data.get(f'image{i}')
                if image_file:
                    Image.objects.create(post=post, image=image_file)
            return redirect("blog:post-list")  
            
    else:
        form = PostForm()

    return render(request, "forms/post.html", {"form": form})
def post_search(request):
    form = SearchForm(request.GET or None)
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']

        # results1 = Post.published.filter(content__icontains=query)
        # results2 = Post.published.filter(title__icontains=query)

        # results = results1.union(results2)
        # with "Q" we can use and or ...
        # results=Post.published.filter(Q(title__icontains=query)|Q(content__icontains=query))
        
        # full text search or FTS  most data bases are support this future 
        # results = Post.published.annotate(
        #     search=SearchVector('title',weigh='A')+SearchVector('content',weigh='B')
        # ).filter(search=query)
        
        # i hear we use FTS with ranking
        # vector = (
        #     SearchVector('title', weight='A') + 
        #     SearchVector('content', weight='B')
        # )
        # search_query = SearchQuery(query)

        # results = Post.published.annotate(
        #     rank=SearchRank(vector, search_query)
        # ).filter(rank__gte=0.1).order_by('-rank')
    
        # trigram similarity
        # pg_trgm is an extension for postgresSQl
    
        results = Post.published.annotate(
        similarity=TrigramSimilarity('title', query)
        ).filter(similarity__gt=0.3).order_by('-similarity')
    context = {
        'form': form,
        'query':query,
        'Results': results,  
    }
    return render(request, 'blog/post-search.html', context)

@login_required
def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)
    context = {
        'posts': posts
    }
    return render(request, 'blog/profile.html', context)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect("blog:profile")
    return render(request, "forms/delete_post.html", {"post": post})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author==request.user:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save(commit=False)
                post.author=request.user
                Post.Status.DRAFT
                post.save()
                for i in range(1, 3):  # تعداد فیلدهای تصویر
                    image_file = form.cleaned_data.get(f'image{i}')
                    if image_file:
                        Image.objects.create(post=post, image=image_file)
                return redirect("blog:profile")
        else:
            # cuz we want to load fields we use instance=post
            form = PostForm(instance=post)

        return render(request, "forms/post.html", {"form": form, "post": post})
    else:
        return redirect("blog:profile")

@login_required
def delete_image(request, image_id):
    if request.method == "POST":
        image = get_object_or_404(Image, id=image_id)
        post = image.post
        if post.author == request.user:
            image.delete()
    return redirect("blog:edit-post", post_id=post.id)


# we use (django.contrib.auth) for user_login
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['user_name'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('blog:profile')  # به صفحه اصلی یا هر URL دیگری
                else:
                    return HttpResponse("کاربر غیر فعال است")
            else:
                return HttpResponse("پسورد یا نام کاربری درست نیست")
    else:
        form = LoginForm()
    
    return render(request, 'forms/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('blog:login')