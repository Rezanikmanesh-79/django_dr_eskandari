from django.urls import path
from blog import views

# from any ware we can access this file exp: (blog:) cuz of app name
app_name = 'blog'

urlpatterns = [
    path('',views.index,name='index'),
    path("posts/",views.post_list,name="post-list"),
    path('post/<int:pk>/',views.post_detail,name="post_detail"),
]
