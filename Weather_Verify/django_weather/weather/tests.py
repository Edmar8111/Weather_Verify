from django.test import TestCase
from django.urls import path
from . import views
import requests
from bs4 import BeautifulSoup
# Create your tests here.
urlpatterns = [
    path('home', views.home, name='home'),
    path('testes', views.testes, name='testes')
]


def request_dados(estado, cidade):
    response_today = requests.get(f'https://tempo.cptec.inpe.br/{estado}/{cidade}')
    response_today = BeautifulSoup(response_today.text,'html.parser')
    clima_max = response_today.find_all(title='Máxima')
    clima_min = response_today.find_all(title='Mínima')
    validador = response_today.find_all(class_='pt-1')
    for b in validador:
        texto = b.text[10:13]
    if texto.strip()!='DF': 
        for a in clima_max:
            print(f'Máxima: {a.text[0:2]}')
        for a in clima_min:
            print(f'Mínima: {a.text[0:2]}º')
    else:
        print('Error city not found')
        