from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView,UpdateView
from django.urls import reverse_lazy
from social.forms import CustomUserCreationForm,CustomUserEditForm

class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'social/register.html'
    success_url = reverse_lazy('social:login')

class UserEditView(UpdateView):
    form_class = CustomUserEditForm
    template_name = 'social/edit_profile.html'
    success_url = reverse_lazy('social:profile')
    def get_object(self, queryset=None):
        return self.request.user

def profile(request):
    return HttpResponse("Hello, world. You're at the profile page.")