from django.shortcuts import render

from django.views.generic import ListView, DetailView, DeleteView
from .models import BlogArticle


class BlogsList(ListView):
    queryset = BlogArticle.objects.all().order_by('-created_at')
    context_object_name = 'blogs'
    template_name = 'blog/allblogs.html'
    paginate_by = 3


class BlogsDetail(DetailView):
    model = BlogArticle
    pk_url_kwarg = 'id'
    context_object_name = 'blog'
    template_name = 'blog/blog_detail.html'


