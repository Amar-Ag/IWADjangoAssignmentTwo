from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View, ListView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage

from .forms import CreateUserForm, AuthorForm
from .models import Author
from .tokens import account_activation_token


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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            username = form.cleaned_data.get('first_name')
            Author.objects.create(
                user=user,
                name=user.first_name + " " + user.last_name,
            )
            current_site = get_current_site(request)
            mail_subject = 'Activate your BlogSite account.'
            message = render_to_string('author/activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            print(urlsafe_base64_encode(force_bytes(user.pk)),
                  account_activation_token.make_token(user))
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(
                request,
                "  Successfully SignUp! Please activate your account mail has been send to your mail box! ")
            messages.success(request, 'Account created successfully for ' + username)
            return HttpResponseRedirect('/author/login/')

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


@method_decorator(login_required(login_url='/author/login'), name='get')
class LogOutView(View):
    template_name = 'author/login.html'

    def get(self, request):
        logout(request)
        return render(request, self.template_name)


@method_decorator(login_required(login_url='/author/login'), name='get')
class ProfileView(View):
    template_name = 'author/profile.html'

    def get(self, request):
        user = request.user.author
        form = AuthorForm(instance=user)
        # blogs = request.user.author.blogarticle_set.all()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user.author
        form = AuthorForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/author/profile/')

        return render(request, self.template_name, {'form': form})


class AuthorList(ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'blog/authors.html'
    paginate_by = 3


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "  Thank you for your email confirmation. Now you can login to your account.")
            return redirect('author:login')

        else:
            messages.error(request, "   Activation link is invalid!.", fail_silently=True)
            return redirect('author:login')
