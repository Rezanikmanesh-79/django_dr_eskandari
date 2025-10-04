from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from social import views
app_name = 'social'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.profile, name='profile'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('edit-profile/',views.UserEditView.as_view(), name='edit_profile'),
]
