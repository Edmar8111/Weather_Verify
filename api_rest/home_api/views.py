from django.shortcuts import render
from rest_framework import generics
from .models import valores
from .serializers import valoresSerializer
import requests
from bs4 import BeautifulSoup
# Create your views here.

class valores_api(generics.ListCreateAPIView):
    #Esta efetuando a gravação dos valores aleatoriamente BUG
    queryset = valores.objects.all()
    serializer_class = valoresSerializer

def home_0(request):
    if request.method == 'POST':
        valor_cidades = (['Acre','AC'],['Alagoas','AL'],['Amapá','AP'],['Amazonas','AM'],
                     ['Bahia','BA'],['Ceará','CE'],['Distrito Federal','DF'],['Espírito Santo','ES']
                     ,['Goiás','GO'],['Maranhão','MA'],['Mato Grosso','MT'],['Mato Grosso do Sul','MS'],
                     ['Minas Gerais','MG'],['Pará','PA'],['Paraíba','PB'],['Paraná','PR'],['Pernambuco','PE'],
                     ['Piauí','PI'],['Rio de Janeiro','RJ'],['Rio Grande do Norte','RN'],['Rio Grande do Sul','RS'],
                     ['Rondônia','RO'],['Roraima','RR'],['Santa Catarina','SC'],['São Paulo','SP'],['Sergipe','SE'],['Tocantins','TO'])
        
        dados = request.POST['valor_0']
        data0 = request.POST['valor_1']
        for a in valor_cidades:
            if a[0] == dados:
                dados_0 = a[1]
        print(f'Estado: {dados_0}, Cidade: {data0}')
        if dados_0:
            url_api = requests.get(f'https://tempo.cptec.inpe.br/{dados_0.lower()}/{data0}')
            print(f'https://tempo.cptec.inpe.br/{dados_0.lower()}/{data0}')
            raspagem_valor = BeautifulSoup(url_api.text, 'html.parser')
            valor_target = raspagem_valor.find_all(class_='pt-1')
            for recorte_texto in valor_target:
                valor_target = str(recorte_texto.text[10:13]).strip()                                           
            if valor_target == 'DF':
                print('requeste: ',valor_target)
            else:
                print('requeste 200 sucesso')
    return render(request, 'base.html')