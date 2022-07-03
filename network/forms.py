from django import forms

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("text",)
        labels = {'text': False}
        widgets = {'text': forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Write something here...'
        })}
