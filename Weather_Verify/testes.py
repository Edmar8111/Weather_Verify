import requests
from bs4 import BeautifulSoup
from datetime import datetime

response = requests.get('https://www.cptec.inpe.br/previsao-tempo/mt/cuiaba')
response = BeautifulSoup(response.text, 'html.parser')
response = response.find_all(class_='text-primary font-weight-bold')

response_today = requests.get('https://tempo.cptec.inpe.br/mt/cuiaba')
response_today = BeautifulSoup(response_today.text,'html.parser')
response_today = response_today.find_all(title='Máxima')
for a in response_today:
    print(a.text[0:2])

print(datetime.now().strftime('%d/%m/%Y'))

def testes():
    dict_cidades = [{'cidade0':'sigla'},{'cidade':'sigla'}]
    valor = 'cidade0'
    for a in dict_cidades:
        for b in a:
            if valor==b:
                print(a)
testes()