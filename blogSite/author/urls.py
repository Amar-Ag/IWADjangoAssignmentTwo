from django.urls import path
from .views import LoginView, SignupView, LogOutView, AuthorList, ProfileView, ActivateView

app_name = 'author'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('all/', AuthorList.as_view(), name='authors'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
]
