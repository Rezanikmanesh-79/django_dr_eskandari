from django.urls import path
from blog import views
# canonical url is direct adders exp :www.example.com/iphone-16
# from any ware we can access this file exp: (blog:) cuz of app name
app_name = 'blog'

urlpatterns = [
    path('',views.index,name='index'),
    path("posts/",views.post_list,name="post-list"),
    path('post/<int:pk>/',views.post_detail,name="post-detail"),
    path('ticket/',views.ticket,name='ticket'),
    path('post/<int:pk>/comment',views.post_comment,name='comment'),
    path('posts/create',views.create_post_view,name='create-post-view'),
    path('posts_search',views.post_search,name='posts_search'),
    path('profile',views.profile,name="profile")
]
