from django.shortcuts import render
from rest_framework import generics
from .models import valores, Prev_extendida
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
            lista_extendida_max=[]
            lista_extendida_min=[]
            url_api = requests.get(f'https://tempo.cptec.inpe.br/{dados_0.lower()}/{data0}')
            print(f'https://tempo.cptec.inpe.br/{dados_0.lower()}/{data0}')
            raspagem_valor = BeautifulSoup(url_api.text, 'html.parser')
            valor_target = raspagem_valor.find_all(class_='pt-1')
            valor_target_maxima = raspagem_valor.find_all(title='Máxima')
            valor_target_minima = raspagem_valor.find_all(title='Mínima')
            valor_target_prev = raspagem_valor.find_all(alt='Temperatura Mínima')
            valor_target_prev_0 = raspagem_valor.find_all(alt='Temperatura Máxima')
            

            for recorte_texto in valor_target:
                valor_target = str(recorte_texto.text[10:13]).strip()                                           
            for a in valor_target_maxima:
                maxima_list.append(a.text[0:2])
            for a in valor_target_minima:
                minima_list.append(a.text[0:2])
            
            for a in valor_target_prev:
                lista_extendida_min.append(str(a.text[0:2]))
            for a in valor_target_prev_0:
                lista_extendida_max.append(str(a.text[0:2]))
            
            #efetuar a criação da interligação dos dados para o db
            
            
            if valor_target == 'DF':
                print('requeste: ',valor_target)
            else:
                import datetime
                data_atual = datetime.datetime.today()
                validar=0
                valor_id=0
                data_comp = []
                datas_previsao = Prev_extendida.objects.all()
                #buscando validação via id entre bancos
                for id_verificar in valores.objects.all():
                    if id_verificar.nome_cidade==data0 and validar==0:
                        validar+=1
                        valor_id=id_verificar.id
                validar=0
                #executa a inicialização do banco
                if len(datas_previsao)==0:
                    db_init = Prev_extendida(
                        id_valores=1,
                        max_diaria=1,
                        cidade='manaus',
                    )
                    db_init.save()
                else:
                    for verificar in range(1,len(lista_extendida_max[0:7])):
                        data_atual = data_atual.replace(day=data_atual.day+1)
                        data_comp.append(data_atual.strftime('%d/%m/%y'))
                    for integrar_datas in range(0, len(data_comp)):
                        if validar==0:
                            for verificar_datas in datas_previsao:
                                for a in range(0, len(data_comp)):
                                    if verificar_datas.cidade == data0:
                                        if verificar_datas.data_prev == data_comp[a]:
                                            print(f'Info do dia:{verificar_datas.data_prev} salvo')
                                        else:
                                            print(f'valores a serem salvos data: {data_comp[a]} {valor_id}')
                                            if data_comp[a]==data_comp[0]:
                                                dados_info=Prev_extendida(
                                                    id_valores=valor_id,
                                                    cidade=data0,
                                                    sigla=dados_0,
                                                    data_prev=data_comp[0],
                                                    max_diaria=maxima_list[1],
                                                    min_diaria=minima_list[1],
                                                )
                                                dados_info.save()
                                            if data_comp[a]!=data_comp[0] and data_comp[a]!=data_comp[-1]:
                                                dados_info = Prev_extendida(
                                                    id_valores=valor_id,
                                                    cidade=data0,
                                                    data_prev=data_comp[a],
                                                    sigla=dados_0,
                                                    max_diaria=lista_extendida_max[a],
                                                    min_diaria=lista_extendida_min[a]
                                                )
                                                print(lista_extendida_max[a])
                                                print(lista_extendida_min[a])
                                                dados_info.save()
                                            if data_comp[a]==data_comp[-1]:
                                                dados_info = Prev_extendida(
                                                    id_valores=valor_id,
                                                    cidade=data0,
                                                    data_prev=data_comp[-1],
                                                    sigla=dados_0,
                                                    max_diaria=lista_extendida_max[-1],
                                                    min_diaria=lista_extendida_min[-1]
                                                )
                                                dados_info.save()
                                            
                                    
                        validar+=1    
                    
                for data_gerar_delete in datas_previsao:
                    if data_gerar_delete.cidade=='desconhecida' or data_gerar_delete.max_diaria==0:
                        data_gerar_delete.delete()
                
            
                                    #prev_ext = Prev_extendida(
                                    #    id_valores=valor_id.id,
                                    #    cidade=data0,
                                    #    sigla=dados_0,
                                    #    data_prev=data_atual.strftime('%d/%m/%y'),
                                    #    max_diaria = int(maxima_list[1]),
                                    #    min_diaria=int(minima_list[1])
                                    #)
                                    #prev_ext.save()
                                    #print('valor salvo')
                for datas_prev in Prev_extendida.objects.all():
                    print(datas_prev.data_prev)
                    
                #print(data_atual.strftime('%d/%m/%Y'))
                #print(lista_extendida_max[0:4])
                #print(lista_extendida_max[-1:])


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
                print('requeste 200 sucesso')
    return render(request, 'base.html')