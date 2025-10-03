from email.policy import HTTP

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .forms import *
from .models import Ticket, Image, Account
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):
    # posts = Post.published.all()
    # print(posts.first().created_at)
    # comments = Comment.objects.filter(is_active=True)
    # context = {'posts': posts, 'comments': comments}
    context = {}
    return render(request, 'blog/index.html', context)
    # return HttpResponse('Hello guys! Have a good day.')

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request, category=None):
    posts = Post.published.all()

    # Filter by category if provided
    if category:
        posts = posts.filter(category=category)

    # Pagination
    paginator = Paginator(posts, 1)  # 2 posts per page
    page_number = request.GET.get('page', 1)
    message = None

    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        message = 'صفحه ای با این شماره نداریم و آخرین صفحه را نشان داده‌ایم.'
    except PageNotAnInteger:
        posts = paginator.page(1)

    context = {
        'posts': posts,
        'message': message,
        'category': category,
    }

    return render(request, 'blog/post-list.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(is_active=True)

    form = CommentForm()
    context = {'post': post,

               'form': form,
               'comments': comments}
    return render(request, 'blog/post-detail.html', context)


def ticket(request):
    ticket_obj = Ticket.objects.create()
    print(request.POST)
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ticket_obj.message = cd['message']
            ticket_obj.name = cd['name']
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.subject = cd['subject']
            ticket_obj.save()

            return redirect('blog:index')
    else:
        form = TicketForm()
    context = {'form': form}
    return render(request, "forms/ticket.html", context)


@require_POST
def post_comment(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    context = {'post': post, 'comment': comment, 'form': form}

    return render(request, 'forms/comment.html', context)


@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the Post instance with author
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # Create Image objects only if images are provided
            if form.cleaned_data['image1']:
                Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            if form.cleaned_data['image2']:
                Image.objects.create(image_file=form.cleaned_data['image2'], post=post)

            return redirect('blog:index')
        else:
            print(form.errors)
    else:
        form = CreatePostForm()
    return render(request, 'forms/create-post.html', {'form': form, 'is_edit': False})


def post_search(request):
    q = None
    results = []
    form = SearchForm()
    # print(request.GET)

    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            print('1:', form.cleaned_data)
            q = form.cleaned_data['query']
            # search_query = SearchQuery(q)
            # search_vector = SearchVector('title', weight='A') + SearchVector('content', weight='D')
            # # results = Post.published.filter(Q(title__icontains=q) | Q(content__icontains=q))
            # results = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
            results = Post.published.annotate(similarity=TrigramSimilarity('content', q)).filter(
                similarity__gt=0.3).order_by('-similarity')
            print(results)
    context = {'form': form, 'query': q, 'results': results}
    return render(request, 'blog/post-search.html', context)


def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)
    context = {'user': user, 'posts': posts}
    return render(request, 'blog/profile.html', context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile')
    return render(request, 'forms/delete_post.html', {'post': post})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        # دریافت تصاویر موجود پست
        existing_images = list(post.images.all())

        if request.method == "POST":
            form = CreatePostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.status = Post.Status.DRAFT
                post.save()

                # مدیریت تصویر 1
                if form.cleaned_data['image1']:
                    # اگر تصویر جدید انتخاب شده، تصویر قبلی را حذف و جدید را اضافه کن
                    if len(existing_images) > 0:
                        existing_images[0].delete()
                    Image.objects.create(image_file=form.cleaned_data['image1'], post=post)

                # مدیریت تصویر 2
                if form.cleaned_data['image2']:
                    # اگر تصویر جدید انتخاب شده، تصویر قبلی را حذف و جدید را اضافه کن
                    if len(existing_images) > 1:
                        existing_images[1].delete()
                    Image.objects.create(image_file=form.cleaned_data['image2'], post=post)

                return redirect('blog:profile')
        else:
            form = CreatePostForm(instance=post)
    else:
        return redirect('blog:profile')

    return render(request, 'forms/create-post.html', {'form': form, 'post': post, 'is_edit': True})
@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    # بررسی اینکه کاربر مالک پست مربوطه است
    if image.post.author == request.user:
        image.delete()
    return redirect('blog:edit-post', post_id=image.post.id)


def user_login(request):
    if request.method=="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['user_name'], password = cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('blog:profile')
                else:
                    return HttpResponse('کازبر توسط مدیر عیر فعال شده است')
            else:
                return HttpResponse('نام کاربری یا رمز عبور نادرست است')

    else:
        form = LoginForm()
    return render(request, 'forms/login.html',{'form':form})


def user_logout(request):
    logout(request)
    return redirect('blog:index')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Your account has been created successfully! You can now log in.")
            Account.objects.create(user=user)
            return redirect('registration/register_done.html')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def edit_account(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST, request.FILES, instance=request.user)
        account_form = AccountEditForm(request.POST, request.FILES, instance=request.user.account)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            messages.success(request, "Your account was updated successfully!")
            return redirect("profile")  # or another page
    else:
        user_form = UserRegisterForm(instance=request.user)
        account_form = AccountEditForm(instance=request.user.account)

    context = {
        'user_form': user_form,
        'account_form': account_form
    }
    return render(request, 'registration/edit-account.html', context)
