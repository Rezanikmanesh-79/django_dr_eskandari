from django import forms
from blog.models import Ticket,Comment

class TicketForm(forms.Form):
# for just checking (not using database) we use Forms
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('گزارش خطا', 'گزارش خطا'),
        ('انتقاد', 'انتقاد'),
    )

    message = forms.CharField(
        widget=forms.Textarea,
        label='متن پیام',
        required=True,
        max_length=500
    )
    name = forms.CharField(
        max_length=50,
        label='نام',
        required=False
    )
    email = forms.EmailField(  
        label='ایمیل',
        required=False
    )
    phone = forms.CharField(
        label='تلفن',
        required=True,
        max_length=11
    )
    subject = forms.ChoiceField( 
        label='موضوع',
        required=True,
        choices=SUBJECT_CHOICES
    )

    def clean_phone(self):
        # every input in django save in dict called cleaned_data
        phone =self.cleaned_data['phone']
        if phone.isdigit()and len(phone)==11:
            return phone
        else:
            raise forms.ValidationError("تلفن بایید عدد صحیح باشد و طول ان یازده رقم باشد")

class CommentForm(forms.ModelForm):
# in this case we work with date base that why we use ModelForm
    class Meta:
        model=Comment
        fields=('name','email','content')

    def clean_field(self):
        name=self.changed_data['name']
        if len(name)>3:
            return name
        else:
            raise forms.ValidationError("نام وارد شده کوتاه است")
