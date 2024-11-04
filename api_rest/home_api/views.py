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
        if dados_0:
            maxima_list=[]
            minima_list=[]
            url_api = requests.get(f'https://tempo.cptec.inpe.br/{dados_0.lower()}/{data0}')
            print(f'https://tempo.cptec.inpe.br/{dados_0.lower()}/{data0}')
            raspagem_valor = BeautifulSoup(url_api.text, 'html.parser')
            valor_target = raspagem_valor.find_all(class_='pt-1')
            valor_target_maxima = raspagem_valor.find_all(title='Máxima')
            valor_target_minima = raspagem_valor.find_all(title='Mínima')
            for recorte_texto in valor_target:
                valor_target = str(recorte_texto.text[10:13]).strip()                                           
            for a in valor_target_maxima:
                maxima_list.append(a.text[0:2])
            for a in valor_target_minima:
                minima_list.append(a.text[0:2])
            if valor_target == 'DF':
                print('requeste: ',valor_target)
            else:
                from time import sleep
                validar_exec = 0
                #Executa a exclusão de arquivos que não possuem info
                for a in valores.objects.all():
                    if a.nome_cidade == 'desconhecida' or a.maxima==0:
                        a.delete()
                for a in valores.objects.all():
                    if data0 == a.nome_cidade and dados_0 == a.sigla_estado:
                        print('requeste dados')
                        dados = valores.objects.get(pk=a.id)
                        validar_exec=+1
                        return render(request, 
                        'base.html', {'maxima':dados.maxima, 'minima':dados.minima, 'sigla':dados.sigla_estado, 'cidade':dados.nome_cidade.upper})
                sleep(5)
                if validar_exec==0:
                    print('requeste')
                    db_request_save = valores(
                        nome_cidade=str(data0),
                        sigla_estado=str(dados_0),
                        maxima=int(maxima_list[0]),
                        minima=int(minima_list[0]),
                        )
                    db_request_save.save()
                    return render(request, 'base.html', {'maxima':maxima_list[0], 'minima':minima_list[0]})
                
                print('Area de testes')
                print(f'Máxima Hoje:{maxima_list[0]}° Min:{minima_list[0]}°, Máxima Amanha:{maxima_list[1]}°, Min:{minima_list[1]}°')
                print(f'Estado: {dados_0}, Cidade: {data0}')
                print('requeste 200 sucesso')
    return render(request, 'base.html')