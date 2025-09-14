from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list, name='post-list'),
    path('posts/<int:pk>/', views.post_detail, name='post-detail'),
    path('ticket/', views.ticket, name='ticket'),
    path('posts/<int:id>/comment', views.post_comment, name='post-comment'),
    path('create_post/', views.create_post, name="create-post"),
    path('search/',views.post_search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('profile/delete-post/<int:post_id>', views.delete_post, name='delete-post'),
    path('profile/edit-post/<int:post_id>', views.edit_post, name='edit-post'),
    path('profile/delete-image/<int:image_id>', views.delete_image, name='delete-image'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

]
