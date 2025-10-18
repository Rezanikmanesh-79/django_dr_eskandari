from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

app_name='social'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('user/edit', views.edit_user, name='edit-user'),
    path('ticket', views.ticket, name="ticket"),
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
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),

    path('posts/', views.post_list, name='post-list')
]
