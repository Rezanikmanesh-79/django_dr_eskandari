from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Post
from .forms import LoginForm, UserRegisterForm, UserEditForm, TicketForm, CreatePostForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def user_login(request):
    if request.method == "POST":
        print('1')
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            print('2')
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('social:profile')
                else:
                    return HttpResponse('کازبر توسط مدیر عیر فعال شده است')
            else:
                return HttpResponse('نام کاربری یا رمز عبور نادرست است')
        else:
            print('3:', form.errors)

    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    # return redirect('blog:index')
    return HttpResponse('خارج شدید')


def profile(request):
    return HttpResponse('وارد شدید')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Account.object.Create(user=user)
            return render(request, 'registration/register_done.html', {'user': user})
    else:

        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_user(request):

    if request.method == 'POST':

        user_form = UserEditForm(request.POST, instance=request.user)
        # account_form = AccountEditForm(
        #     request.POST,
        #     instance=request.user.account,
        #     files=request.FILES
        # )

        if user_form.is_valid():

            user_form.save()
            # account_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        # account_form = AccountEditForm(instance=request.user.account)

    context = {'user_form': user_form, }
    return render(request, 'registration/edit-user.html', context)


def ticket(request):
    sent = False
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = cd['subject']
            message = cd['message']
            # email=cd['email']
            send_mail(subject, message, 'python.django.1404.1@gmail.com', ['eskandary.a@gmail.com'], fail_silently=False)
            sent = True
    else:
        form = TicketForm()

    return render(request, 'forms/ticket.html', {'form': form, 'sent': sent})


def post_list(request, tag_slug=None):
    posts = Post.objects.all().order_by('-created')

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 1)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # AJAX Load More
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(
            request,
            'social/list-ajax.html',
            {'posts': posts, 'tag': tag}
        )

    return render(
        request,
        'social/list.html',
        {'posts': posts, 'tag': tag}
    )



@login_required
def post_create(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            # Save the Post instance with author
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save tags

            # # Create Image objects only if images are provided
            # if form.cleaned_data['image1']:
            #     Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            # if form.cleaned_data['image2']:
            #     Image.objects.create(image_file=form.cleaned_data['image2'], post=post)

            return redirect('social:post-list')
        else:
            print(form.errors)
    else:
        form = CreatePostForm()
    return render(request, 'forms/create-post.html', {'form': form, 'is_edit': False})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'social/detail.html', {'post': post})


@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    post_like_count = post.likes.count()
    response_data = {
        'liked': liked,
        'post_like_count': post_like_count,
    }
    return JsonResponse(response_data)


@login_required
@require_POST
def post_save(request):
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post =Post.objects.get(id=post_id)
        user = request.user
        if user in post.save_by.all():
            post.save_by.remove(user)
            saved = False
        else:
            post.save_by.add(user)
            saved = True
        return JsonResponse({"saved":saved})
    return JsonResponse({'error': 'Invalid post_id !'})