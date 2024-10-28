from django.test import TestCase
from django.urls import path
from django.shortcuts import redirect
from . import views
import requests
from bs4 import BeautifulSoup

# Create your tests here.
urlpatterns = [
    path('home', views.home, name='home'),
    path('testes', views.testes, name='testes')
]


        