from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from .models import BlogArticle
from .forms import CreateBlogForm


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


def create_slug(string):
    s = string.lower()
    words = s.split(' ')
    slug = '-'.join(words)
    return slug


@method_decorator(login_required, name='dispatch')
class BlogsCreate(CreateView):
    form_class = CreateBlogForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user.author
        form.instance.slug = create_slug(form.cleaned_data['title'])
        form.save()
        form.save_m2m()
        return super(BlogsCreate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class BlogsUpdate(UserPassesTestMixin, UpdateView):
    model = BlogArticle
    pk_url_kwarg = 'id'
    form_class = CreateBlogForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user.author
        form.instance.slug = create_slug(form.cleaned_data['title'])
        form.save()
        form.save_m2m()
        return super(BlogsUpdate, self).form_valid(form)

    def test_func(self):
        article = self.get_object()
        if self.request.user.author == article.author:
            return True
        return False


@method_decorator(login_required, name='dispatch')
class BlogsDelete(UserPassesTestMixin, DeleteView):
    model = BlogArticle
    pk_url_kwarg = 'id'
    context_object_name = 'blog'
    template_name = 'blog/delete.html'
    success_url = '/blog/'

    def test_func(self):
        article = self.get_object()
        if self.request.user.author == article.author:
            return True
        return False
