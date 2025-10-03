from django import forms
from blog.models import Comment, Post, User


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (('پیشنهاد', 'پیشنهاد'), ('گزارش خطا', 'گزارش خطا'), ('انتقاد', 'انتقاد'))
    message = forms.CharField(widget=forms.Textarea, label='متن تیکت', required=True, max_length=500)
    name = forms.CharField(label='نام', required=False, max_length=50)
    email = forms.EmailField(label='ایمیل', required=False)
    phone = forms.CharField(label='تلقن', required=True, max_length=11)
    subject = forms.ChoiceField(label='موضوع', required=True, choices=SUBJECT_CHOICES)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone.isdigit() and len(phone) == 11:
            return phone
        else:
            raise forms.ValidationError(' تلفن باید عدد صحیح باشد و طول آن 11 رقم باشد.')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content',)

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError('نام وارد شده کوتاه است')
        else:
            return name


class CreatePostForm(forms.ModelForm):
    image1 = forms.ImageField(label='تصویر 1', required=False)
    image2 = forms.ImageField(label='تصویر 2', required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'read_time']


class SearchForm(forms.Form):
    query = forms.CharField(label='جستجو', max_length=100)


class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=250, required=True)
    password = forms.CharField(max_length=250,required=True, widget=forms.PasswordInput)

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
