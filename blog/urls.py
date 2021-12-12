from django.contrib import admin
from django.urls import path, include

from .import views

urlpatterns = [
    path('Blogcomment/', views.Blogcomment, name='Blogcomment'),
    path('', views.Bloghome, name='Bloghome'),
    path('<str:slug>', views.Blogpost, name='Blogpost'),

]
