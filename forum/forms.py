from django import forms
from .models import Post, Thread

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

class PostThread(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'description', 'content']
        widgets = {
            'title': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок',
                'rows' : 1,
                'oninput' : 'autoResize(this)',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опис теми',
                'rows' : 2,
                'oninput' : 'autoResize(this)',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст теми',
                'rows': 4,
                'oninput' : 'autoResize(this)',
            })
        }