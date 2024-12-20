from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text_post']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text_post': forms.Textarea(attrs={'class': 'form-control'})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Вы превысили количество символов в заголовке')

        return title
    
    def clean_text_post(self):
        title, text_post = self.cleaned_data['title'], self.cleaned_data['text_post']
        if title == text_post:
            raise ValidationError('Заголовок и текст не должны совпадать')
        return text_post
