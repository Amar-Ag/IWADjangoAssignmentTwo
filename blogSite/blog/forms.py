from django import forms
from .models import BlogArticle


class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = BlogArticle
        fields = ['title', 'content']
