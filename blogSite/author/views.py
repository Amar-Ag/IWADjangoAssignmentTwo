from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm
from .models import Author


class SignupView(View):
    form = CreateUserForm()
    template_name = 'author/signup.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/blog/')
        else:
            form = self.form
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('email')
            Author.objects.create(
                user=user,
            )
            messages.success(request, 'Account created successfully for ' + user)
            return HttpResponseRedirect('/blog/')

        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'author/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/blog/')
        else:
            return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/blog/')
        else:
            messages.error(request, 'Username or password is incorrect.')

        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class LogOutView(View):
    template_name = 'author/login.html'

    def get(self, request):
        logout(request)
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'author/profile.html'

    def get(self, request):
        blogs = request.user.author.blogarticle_set.all()
        context = {'blogs': blogs}
        return render(request, self.template_name, context)


class AuthorList(ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'blog/authors.html'
    paginate_by = 3
