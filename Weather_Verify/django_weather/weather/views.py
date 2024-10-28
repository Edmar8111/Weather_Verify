from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from . import tests
# Create your views here.

@csrf_exempt
def home(request):
    if request.method=='POST':
        data = json.loads(request.body)
        lista=[]
        def test():
            global lista
            print(lista)
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
        tests.request_dados(data1.lower(),data0)
        print(response_today.status_code)
        if response_today.status_code==200:
            print('requeste bem sucedida')
            print(lista)
    return render(request, "base.html")

@csrf_exempt
def testes(request):
    
    print('requeste')
    return redirect(request, home)
    