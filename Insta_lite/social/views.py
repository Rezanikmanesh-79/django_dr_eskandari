from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Remove unused import; add specific model imports if needed, e.g.:
from .models import Post
from .forms import LoginForm, UserRegisterForm, UserEditForm, TicketForm
from django.core.mail import send_mail
from taggit.models import Tag


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


def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    context = {
        'posts': posts,
        'tag': tag
    }
    return render(request, 'social/list.html', context)
@login_required

def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            # For example, send an email or save the ticket
            form.save()
            return HttpResponse('Ticket submitted successfully!')
    else:
        form = TicketForm()

    return render(request, 'social/ticket.html', {'form': form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # ✅ Save tags and other many-to-many relationships
            return redirect('social:post-list')
    else:
        form = PostForm()

    return render(request, 'social/post_form.html', {'form': form})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'social/post_detail.html', {'post': post})