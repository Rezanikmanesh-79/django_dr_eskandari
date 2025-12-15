from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'social'

urlpatterns = [

    # ============================================================
    #                     Auth & User Account
    # ============================================================

    # صفحه ورود
    path('login/', views.user_login, name='login'),

    # خروج از حساب
    path('logout/', views.user_logout, name='logout'),

    # ثبت نام
    path('register/', views.register, name='register'),

    # ویرایش پروفایل کاربر
    path('user/edit/', views.edit_user, name='edit-user'),

    # پروفایل خود کاربر → صفحه پیش‌فرض سایت
    path('', views.profile, name='profile'),


    # ============================================================
    #                     Password Management
    # ============================================================

    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(success_url='done'),
        name='password-change'
    ),

    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password-change-done'
    ),

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(success_url='done'),
        name='password-reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password-reset-done'
    ),

    path(
        'password-reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            success_url='/social/password-reset/complete'
        ),
        name="password-reset-confirm"
    ),

    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete"
    ),


    # ============================================================
    #                     Post System
    # ============================================================

    # لیست پست‌ها
    path('posts/', views.post_list, name='post-list'),

    # لیست پست‌ها بر اساس تگ (توجه: مسیر اصلاح شده!)
    path('tag/<slug:tag_slug>/', views.post_list, name='post-list-by-tag'),

    # ایجاد پست جدید
    path('posts/create/', views.post_create, name='post-create'),

    # مشاهده جزئیات پست
    path('posts/<int:id>/', views.post_detail, name='post_detail'),

    # AJAX: لایک/آنلایک
    path('ajax/like/', views.post_like, name='like_post'),

    # AJAX: ذخیره/حذف ذخیره پست
    path('ajax/save_post/', views.save_post, name="save_post"),


    # ============================================================
    #                     User List & Profiles
    # ============================================================

    # لیست همه کاربران
    path('users/', views.user_list, name='user-list'),

    # صفحه پروفایل دیگران
    path('users/<str:username>/', views.user_detail, name='user_detail'),

    # فالو/آنفالو (AJAX)
    path('ajax/follow/', views.user_follow, name='user_follow'),

    # لیست فالوئرها
    path('followers/<str:username>/', views.followers_view, name='user_followers'),

    # لیست فالوئینگ
    path('following/<str:username>/', views.following_view, name='user_following'),


    # ============================================================
    #                     Social Actions (AJAX)
    # ============================================================

    # بلاک/آن‌بلاک (AJAX)
    path('ajax/toggle-block/', views.toggle_block_user, name='toggle_block_user'),

    # ریپورت کاربر (AJAX)
    path('ajax/report/', views.report_user, name='report_user'),


    # ============================================================
    #                     Contact / Ticket Form
    # ============================================================

    path('ticket/', views.ticket, name="ticket"),
]
# =====================================================================
