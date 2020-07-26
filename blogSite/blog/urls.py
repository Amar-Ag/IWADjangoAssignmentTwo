from . import views
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', views.BlogsList.as_view(), name='home'),
    path('detail/<slug:slug>/', views.BlogsDetail.as_view(), name='detail'),
    path('create/', views.BlogsCreate.as_view(), name='create'),
    path('update/<slug:slug>/', views.BlogsUpdate.as_view(), name='update'),
    path('delete/<slug:slug>/confirm', views.BlogsDelete.as_view(), name='delete'),
]
