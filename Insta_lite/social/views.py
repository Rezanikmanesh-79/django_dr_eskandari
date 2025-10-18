from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Remove unused import; add specific model imports if needed, e.g.:
from .models import Post
from .forms import LoginForm, UserRegisterForm, UserEditForm, TicketForm
from django.core.mail import send_mail


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


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'social/list.html', context)

