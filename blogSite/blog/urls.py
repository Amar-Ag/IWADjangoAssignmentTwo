from . import views
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', views.BlogsList.as_view(), name='home'),
    path('detail/<slug:slug>/', views.BlogsDetail.as_view(), name='detail'),
]
