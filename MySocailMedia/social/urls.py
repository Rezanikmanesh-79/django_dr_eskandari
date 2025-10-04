from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from social import views
app_name = 'social'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.profile, name='profile'),
]
