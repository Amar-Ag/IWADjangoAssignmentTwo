from django.urls import path
from .views import LoginView, SignupView, LogOutView, AuthorList

app_name = 'author'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('authors/', AuthorList.as_view(), name='authors'),
]
