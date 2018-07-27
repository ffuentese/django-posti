from django import forms
from .models import Post
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from nocaptcha_recaptcha.fields import NoReCaptchaField



class PostForm(forms.ModelForm):
    captcha = NoReCaptchaField()

    class Meta:
        model = Post
        fields = ('title', 'text')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': SummernoteWidget(attrs={'class': 'form-control',
                                            'summernote': {'width': '100%', 'placeholder': 'Texto'}}),

        }

class UpdateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': SummernoteWidget(attrs={'class': 'form-control',
                                            'summernote': {'width': '100%', 'placeholder': 'Texto'}}),

        }