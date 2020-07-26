from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import LoginView, SignupView, LogOutView, AuthorList, ProfileView

app_name = 'author'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('all/', AuthorList.as_view(), name='authors'),
    path('profile/', ProfileView.as_view(), name='profile'),

]
