from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from bs4 import BeautifulSoup


# Create your views here.
maxima = ''
@csrf_exempt
def home(request):
    #passar essa function para a views
    
    def request_dados(estado, cidade):
        global maxima, minima
        response_today = requests.get(f'https://tempo.cptec.inpe.br/{str(estado).lower()}/{str(cidade).lower()}')
        response_today = BeautifulSoup(response_today.text,'html.parser')
        clima_max = response_today.find_all(title='Máxima')
        clima_min = response_today.find_all(title='Mínima')
        validador = response_today.find_all(class_='pt-1')
        for b in validador:
            texto = b.text[10:13]
        if texto.strip()!='DF': 
            valor_0 = []
            valor_0.append([a.text for a in clima_max])
            valor_0.append([a.text for a in clima_min])
            #return print(f'Máxima:{valor_0[0][0]}', f'Mínima:{valor_0[1][0]}')
            maxima = valor_0[0][0]
            minima = valor_0[1][0]
            return redirect(to=home)
        else:
            print('Error city not found')

    if request.method=='POST':
        data = json.loads(request.body)        
        valor_cidades = [{'Acre':'AC'},{'Alagoas':'AL'},{'Amapá':'AP'},{'Amazonas':'AM'},
                     {'Bahia':'BA'},{'Ceará':'CE'},{'Distrito Federal':'DF'},{'Espírito Santo':'ES'}
                     ,{'Goiás':'GO'},{'Maranhão':'MA'},{'Mato Grosso':'MT'},{'Mato Grosso do Sul':'MS'},
                     {'Minas Gerais':'MG'},{'Pará':'PA'},{'Paraíba':'PB'},{'Paraná':'PR'},{'Pernambuco':'PE'},
                     {'Piauí':'PI'},{'Rio de Janeiro':'RJ'},{'Rio Grande do Norte':'RN'},{'Rio Grande do Sul':'RS'},
                     {'Rondônia':'RO'},{'Roraima':'RR'},{'Santa Catarina':'SC'},{'São Paulo':'SP'},{'Sergipe':'SE'},{'Tocantins':'TO'}]
        data1 = data.get('data')
        data0=data.get('data0')
        #efetua o tratameto dos dados referente ao estado
        for a in valor_cidades:
            for b in a:
                if data1==b:
                    data1=str(a)
        ini=data1.find(':')
        data1=data1[ini:]
        data1=data1[3:5]
        response_today = requests.get(f'https://tempo.cptec.inpe.br/{data1.lower()}/{data0}')
        request_dados(data1.lower(),data0)
        print(maxima)
        print(response_today.status_code)
        if response_today.status_code==200:
            print('requeste bem sucedida')
        
        #utilizar ou o name ou o text no tag requisitando os valores de uma tag especifica
        url_s = requests.get('https://previsaonumerica.cptec.inpe.br/novo/meteograma/wrf7/mt/cuiaba')
        valor = BeautifulSoup(url_s.text, 'html.parser')
        tags = [tag.name for tag in valor.find_all()]
        print(tags)
    if maxima:
        return render(request, "base.html", {'maxima':maxima, 'minima':minima})
    
    return render(request, "base.html")

@csrf_exempt
def testes(request):
    
    print('requeste')
    return render(request, 'testes.html')
    