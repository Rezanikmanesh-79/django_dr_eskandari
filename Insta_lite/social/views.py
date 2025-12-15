"""
views.py
---------
در این فایل تمام view های مربوط به:
- احراز هویت (login / logout / register)
- پروفایل کاربر
- لیست و جزئیات پست‌ها
- ایجاد پست
- لایک و ذخیره‌سازی پست (AJAX)
- فالو / آنفالو (AJAX)
- بلاک / آن‌بلاک (AJAX)
- ریپورت کاربر (AJAX)
قرار داده شده‌اند.

در این مرحله فقط از Django معمولی (Template-based) استفاده می‌کنیم،
و در مراحل بعدی همین ساختار را به نسخه DRF (API) تبدیل می‌کنیم.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from taggit.models import Tag

from .models import (
    Post,
    User,
    Contact,
    Report,
    BlockRelation,
)
from .forms import (
    LoginForm,
    UserRegisterForm,
    UserEditForm,
    TicketForm,
    CreatePostForm,
)


# =====================================================================
#                    توابع کمکی (Helper functions)
# =====================================================================

def is_interaction_blocked(user1: User, user2: User) -> bool:
    """
    بررسی می‌کند آیا تعامل بین دو کاربر باید ممنوع باشد یا نه.

    اگر یکی دیگری را بلاک کرده باشد → خروجی True می‌شود.
    این تابع را در لایک، فالو، مشاهده پروفایل، مشاهده پست و ... استفاده می‌کنیم.
    """
    if not user1.is_authenticated or not user2.is_authenticated:
        return False

    # user1 طرف ما (request.user) است
    # has_blocked => user1 این کاربر را بلاک کرده؟
    # is_blocked  => user1 توسط این کاربر بلاک شده؟
    return user1.has_blocked(user2) or user1.is_blocked(user2)


# =====================================================================
#                        احراز هویت: لاگین
# =====================================================================

def user_login(request):
    """
    نمایش فرم لاگین و پردازش ورود کاربر.

    - در صورت GET: فقط فرم نمایش داده می‌شود.
    - در صورت POST: داده‌ها اعتبارسنجی می‌شوند.
    """
    if request.method == "POST":
        # LoginForm معمولا بر اساس AuthenticationForm نوشته می‌شود
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # اگر فرم معتبر بود، کاربر از طریق خود فرم شناسایی می‌شود
            user = form.get_user()
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, "با موفقیت وارد شدید.")
                return redirect('social:profile')
            else:
                messages.error(request, "حساب کاربری شما غیرفعال است.")
        else:
            # در صورت نامعتبر بودن فرم، خطاها در قالب نمایش داده می‌شوند
            messages.error(request, "نام کاربری یا رمز عبور نادرست است.")
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


# =====================================================================
#                        خروج از حساب کاربری
# =====================================================================

@login_required
def user_logout(request):
    """
    خروج کاربر از حساب کاربری و هدایت به صفحه ورود.
    """
    logout(request)
    messages.info(request, "از حساب کاربری خود خارج شدید.")
    return redirect('social:login')  # فرض بر این‌که نام url لاگین این است


# =====================================================================
#                            پروفایل کاربر
# =====================================================================

@login_required
def profile(request):
    """
    صفحه پروفایل کاربر فعلی (خود کاربر).

    در این صفحه:
    - پست‌های ذخیره‌شده کاربر نمایش داده می‌شوند.
    - می‌توان بعدا اطلاعات دیگری هم اضافه کرد.
    """
    user = request.user
    saved_posts = user.saved_posts.all()  # related_name = 'saved_posts' در مدل Post

    context = {
        'user': user,
        'saved_posts': saved_posts,
    }
    return render(request, 'social/profile.html', context)


# =====================================================================
#                    ثبت‌نام کاربر جدید (Register)
# =====================================================================

def register(request):
    """
    ثبت‌نام کاربر جدید.

    - اگر متد POST باشد → فرم پردازش شده و در صورت اعتبار ذخیره می‌شود.
    - در غیر این صورت فقط فرم خالی نمایش داده می‌شود.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # هنوز ذخیره نکنیم تا بتوانیم روی پسورد کار کنیم
            user = form.save(commit=False)
            # حتماً از set_password برای هش کردن پسورد استفاده می‌کنیم
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "ثبت‌نام با موفقیت انجام شد.")
            return render(request, 'registration/register_done.html', {'user': user})
        else:
            messages.error(request, "لطفاً خطاهای فرم را برطرف کنید.")
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})


# =====================================================================
#                  ویرایش اطلاعات کاربری (Edit Profile)
# =====================================================================

@login_required
def edit_user(request):
    """
    ویرایش اطلاعات پروفایل کاربر جاری.

    این ویو از فرم UserEditForm استفاده می‌کند که بر اساس مدل User ساخته شده.
    """
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "اطلاعات پروفایل شما با موفقیت به‌روزرسانی شد.")
            return redirect('social:profile')
        else:
            messages.error(request, "لطفاً خطاهای فرم را برطرف کنید.")
    else:
        user_form = UserEditForm(instance=request.user)

    context = {'user_form': user_form}
    return render(request, 'registration/edit-user.html', context)


# =====================================================================
#                        فرم تیکت / تماس با ما
# =====================================================================

def ticket(request):
    """
    فرم ارسال پیام/تیکت به مدیر سیستم.

    پس از ارسال موفق، متغیر 'sent' برابر True می‌شود تا
    در قالب پیام موفقیت نمایش داده شود.
    """
    sent = False
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = cd['subject']
            message = cd['message']
            # ایمیل فرستنده در اینجا هاردکد شده است، در عمل بهتر است از settings گرفته شود.
            send_mail(
                subject,
                message,
                'python.django.1404.1@gmail.com',
                ['eskandary.a@gmail.com'],
                fail_silently=False
            )
            sent = True
            messages.success(request, "پیام شما ارسال شد.")
    else:
        form = TicketForm()

    return render(request, 'forms/ticket.html', {'form': form, 'sent': sent})


# =====================================================================
#                        لیست پست‌ها + فیلتر تگ + صفحه‌بندی
# =====================================================================

def post_list(request, tag_slug=None):
    """
    لیست پست‌ها با قابلیت:

    - فیلتر براساس تگ
    - صفحه‌بندی (pagination)
    - پشتیبانی از AJAX برای لود بیشتر (infinite scroll یا load more)
    - فیلتر بر اساس بلاک بودن کاربر
    """
    posts = Post.objects.select_related('author').all()

    # فیلتر بر اساس تگ (اختیاری)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    # اگر کاربر لاگین کرده باشد، پست‌های مربوط به بلاک‌ها را حذف می‌کنیم
    if request.user.is_authenticated:
        blocked_ids = request.user.blocked_users.values_list('id', flat=True)
        blocked_by_ids = request.user.blocked_by.values_list('id', flat=True)

        # حذف پست‌هایی که نویسنده‌شان بلاک شده یا کاربر ما را بلاک کرده
        posts = posts.exclude(author__id__in=blocked_ids).exclude(author__id__in=blocked_by_ids)

    # صفحه‌بندی
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 5)  # مثلا 5 پست در هر صفحه
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    # اگر درخواست AJAX باشد (مثلاً برای infinite scroll)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'social/list-ajax.html', {'posts': posts_page})

    context = {
        'posts': posts_page,
        'tag': tag,
    }
    return render(request, 'social/list.html', context)


# =====================================================================
#                        ایجاد پست جدید
# =====================================================================

@login_required
def post_create(request):
    """
    ایجاد پست جدید توسط کاربر لاگین کرده.

    - در POST: فرم بررسی و در صورت صحت ذخیره می‌شود.
    - در GET: فرم خالی نمایش داده می‌شود.
    """
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # تنظیم نویسنده پست
            post.save()
            form.save_m2m()  # برای ذخیره تگ‌ها و سایر روابط ManyToMany

            messages.success(request, "پست شما با موفقیت ایجاد شد.")
            return redirect('social:post-list')
        else:
            messages.error(request, "لطفاً خطاهای فرم را برطرف کنید.")
    else:
        form = CreatePostForm()

    return render(request, 'forms/create-post.html', {'form': form, 'is_edit': False})


# =====================================================================
#                        جزئیات یک پست
# =====================================================================

def post_detail(request, id):
    """
    صفحه نمایش جزئیات یک پست.

    اگر ارتباط بین نویسنده پست و کاربر جاری بلاک باشد،
    نمایش پست ممنوع می‌شود.
    """
    post = get_object_or_404(Post.objects.select_related('author'), id=id)

    # اگر کاربر لاگین است و بلاک وجود دارد → 403
    if request.user.is_authenticated and is_interaction_blocked(request.user, post.author):
        return HttpResponseForbidden("دسترسی به این پست برای شما مسدود است.")

    return render(request, 'social/detail.html', {'post': post})


# =====================================================================
#                        لایک کردن/برداشتن لایک (AJAX)
# =====================================================================

@login_required
@require_POST
def post_like(request):
    """
    ویوی AJAX برای لایک و آن‌لایک کردن پست.

    ورودی: post_id در POST
    خروجی: JSON شامل:
        - liked: آیا الان لایک شده یا نه
        - post_like_count: تعداد کل لایک‌ها
    """
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)

    # اگر بین کاربر و نویسنده پست بلاک است، اجازه لایک نداریم
    if is_interaction_blocked(request.user, post.author):
        return JsonResponse(
            {'error': 'interaction_blocked'},
            status=403
        )

    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        # بهتر است کاربر نتواند پست خودش را لایک کند (اختیاری)
        if post.author == user:
            return JsonResponse({'error': 'cannot_like_own_post'}, status=400)
        post.likes.add(user)
        liked = True

    post_like_count = post.likes.count()
    response_data = {
        'liked': liked,
        'post_like_count': post_like_count,
    }
    return JsonResponse(response_data)


# =====================================================================
#                        ذخیره / برداشتن ذخیره پست (AJAX)
# =====================================================================

@login_required
@require_POST
def save_post(request):
    """
    ویوی AJAX برای ذخیره یا حذف ذخیره پست توسط کاربر.

    ورودی: post_id
    خروجی: JSON شامل:
        - saved: وضعیت جدید ذخیره بودن پست
    """
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = get_object_or_404(Post, id=post_id)

        # چک بلاک
        if is_interaction_blocked(request.user, post.author):
            return JsonResponse(
                {'status': 'error', 'message': 'interaction_blocked'},
                status=403
            )

        user = request.user
        if user in post.save_by.all():
            post.save_by.remove(user)
            saved = False
        else:
            post.save_by.add(user)
            saved = True
        return JsonResponse({'saved': saved})

    return JsonResponse({'error': 'Invalid post id!'}, status=400)


# =====================================================================
#                        لیست کاربران
# =====================================================================

@login_required
def user_list(request):
    """
    نمایش لیست کاربران (به جز خود کاربر جاری).

    کاربران بلاک‌شده یا بلاک‌کننده حذف می‌شوند.
    """
    users = User.objects.exclude(id=request.user.id)

    blocked_ids = request.user.blocked_users.values_list('id', flat=True)
    blocked_by_ids = request.user.blocked_by.values_list('id', flat=True)

    users = users.exclude(id__in=blocked_ids).exclude(id__in=blocked_by_ids)

    return render(request, 'user/user_list.html', {'users': users})


# =====================================================================
#                        جزئیات کاربر (پروفایل دیگران)
# =====================================================================

@login_required
def user_detail(request, username):
    """
    صفحه پروفایل یک کاربر دیگر.

    اگر بین دو کاربر رابطه بلاک باشد، دسترسی ممنوع می‌شود.
    """
    user_obj = get_object_or_404(User, username=username)

    # اگر رابطه بلاک وجود دارد → 403
    if is_interaction_blocked(request.user, user_obj):
        return HttpResponseForbidden("دسترسی به این پروفایل برای شما مسدود است.")

    return render(request, 'user/user_detail.html', {'user': user_obj})


# =====================================================================
#                        فالو / آنفالو (AJAX)
# =====================================================================

@login_required
@require_POST
def user_follow(request):
    """
    ویوی AJAX برای دنبال کردن یا آنفالو کردن یک کاربر.

    ورودی: id (شناسه کاربر هدف)
    خروجی: JSON شامل:
        - follow: وضعیت جدید (True = اکنون در حال فالو)
        - following_count: تعداد کسانی که او فالو می‌کند
        - followers_count: تعداد فالوئرهای او
    """
    user_id = request.POST.get('id')
    if user_id is not None:
        try:
            target_user = User.objects.get(id=user_id)

            # جلوگیری از فالو کردن خود
            if target_user == request.user:
                return JsonResponse(
                    {'error': 'cannot_follow_self'},
                    status=400
                )

            # جلوگیری از تعامل در صورت بلاک
            if is_interaction_blocked(request.user, target_user):
                return JsonResponse(
                    {'error': 'interaction_blocked'},
                    status=403
                )

            # اگر قبلاً فالو کرده بود → آنفالو
            if request.user in target_user.followers.all():
                Contact.objects.filter(
                    user_from=request.user,
                    user_to=target_user
                ).delete()
                follow = False
            else:
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=target_user
                )
                follow = True

            following_count = target_user.following.count()
            followers_count = target_user.followers.count()
            context = {
                'follow': follow,
                'following_count': following_count,
                'followers_count': followers_count,
            }
            return JsonResponse(context)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist!'}, status=404)

    return JsonResponse({'error': 'Invalid user id!'}, status=400)


# =====================================================================
#                        لیست فالوئرها
# =====================================================================

@login_required
def followers_view(request, username):
    """
    نمایش فالوئرهای یک کاربر.

    کاربران بلاک‌شده توسط request.user از لیست حذف می‌شوند.
    همچنین می‌توانستیم کسانی که ما را بلاک کرده‌اند هم حذف کنیم.
    """
    user_obj = get_object_or_404(User, username=username)

    followers = user_obj.followers.all()

    # حذف کسانی که ما آن‌ها را بلاک کرده‌ایم
    followers = followers.exclude(
        id__in=request.user.blocked_users.values_list('id', flat=True)
    ).exclude(
        id__in=request.user.blocked_by.values_list('id', flat=True)
    )

    return render(request, 'user/followers.html', {'followers': followers})


# =====================================================================
#                        لیست کسانی که کاربر دنبال می‌کند
# =====================================================================

@login_required
def following_view(request, username):
    """
    نمایش لیست کاربرانی که یک کاربر آن‌ها را دنبال می‌کند.
    مشابه followers_view، افراد بلاک‌شده از لیست حذف می‌شوند.
    """
    user_obj = get_object_or_404(User, username=username)

    following = user_obj.following.all()

    following = following.exclude(
        id__in=request.user.blocked_users.values_list('id', flat=True)
    ).exclude(
        id__in=request.user.blocked_by.values_list('id', flat=True)
    )

    return render(request, 'user/following.html', {'following': following})


# =====================================================================
#                        بلاک / آن‌بلاک (AJAX)
# =====================================================================

@login_required
@require_POST
def toggle_block_user(request):
    """
    ویوی AJAX برای بلاک یا آن‌بلاک کردن یک کاربر.

    ورودی: user_id
    خروجی: JSON شامل:
        - status: ok / error
        - action: "blocked" یا "unblocked"
    """
    user_id = request.POST.get("user_id")
    try:
        target = User.objects.get(id=user_id)
    except (User.DoesNotExist, TypeError, ValueError):
        return JsonResponse(
            {"status": "error", "message": "User not found."},
            status=404
        )

    # جلوگیری از بلاک کردن خود یا ادمین اصلی (به دلخواه)
    if target == request.user or target.is_superuser:
        return JsonResponse(
            {"status": "error", "message": "Invalid operation."},
            status=400
        )

    # اگر قبلاً بلاک شده → آن‌بلاک
    if request.user.has_blocked(target):
        BlockRelation.objects.filter(
            blocker=request.user,
            blocked=target
        ).delete()
        action = "unblocked"
    else:
        BlockRelation.objects.create(
            blocker=request.user,
            blocked=target
        )
        action = "blocked"

    return JsonResponse({"status": "ok", "action": action})


# =====================================================================
#                        ریپورت کاربر (AJAX)
# =====================================================================

@login_required
@require_POST
def report_user(request):
    """
    ویوی AJAX برای گزارش (Report) کردن یک کاربر.

    ورودی‌ها:
        - user_id
        - reason (اختیاری ولی بهتر است خالی نباشد)

    نکته: در مدل Report، UniqueConstraint داریم
    که اجازه نمی‌دهد یک کاربر چندبار یک نفر را گزارش کند.
    """
    user_id = request.POST.get("user_id")
    reason = request.POST.get("reason", "").strip()

    # نکته آموزشی: بهتر است reason خالی نباشد،
    # اما این به سیاست اپلیکیشن بستگی دارد.
    if not user_id:
        return JsonResponse(
            {"status": "error", "message": "User id is required."},
            status=400
        )

    try:
        target = User.objects.get(id=user_id)
    except (User.DoesNotExist, ValueError, TypeError):
        return JsonResponse(
            {"status": "error", "message": "User not found."},
            status=404
        )

    if target == request.user:
        return JsonResponse(
            {"status": "error", "message": "You can't report yourself."},
            status=400
        )

    # اگر یکی دیگری را بلاک کرده، شاید هنوز اجازه ریپورت بدهیم (به سیاست سیستم بستگی دارد)
    # اینجا اجازه می‌دهیم، چون ممکن است دلیل بلاک، رفتار بد اما قابل گزارش باشد.

    # ایجاد رکورد ریپورت
    # اگر unique constraint خطا بدهد (در صورت دوبار report):
    # بهتر است try/except روی IntegrityError بگذاریم.
    from django.db import IntegrityError
    try:
        Report.objects.create(
            reporter=request.user,
            reported=target,
            reason=reason
        )
        return JsonResponse(
            {"status": "ok", "message": "User reported."}
        )
    except IntegrityError:
        # یعنی قبلاً این کاربر را گزارش کرده‌ایم
        return JsonResponse(
            {"status": "error", "message": "You have already reported this user."},
            status=400
        )
# =====================================================================