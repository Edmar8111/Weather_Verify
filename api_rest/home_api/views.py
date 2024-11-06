from django.shortcuts import render
from rest_framework import generics
from .models import valores, Prev_extendida
from .serializers import valoresSerializer
import requests
from bs4 import BeautifulSoup
from time import sleep
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
                def requisitar_prev():
                    import datetime
                    data_atual = datetime.datetime.today()
                    data_comp=['11/11/11']
                    cidade_count=[]
                    datas_cidade=[]
                    id_cidade=0
                    #efetua a requisição do id da cidade referente no banco de dados
                    for id_cidade_0 in valores.objects.all():
                        if id_cidade_0.nome_cidade==data0:
                            id_cidade=id_cidade_0.id
                    print(id_cidade) 
                    #autenticação de data e implementação na lista
                    for data_0 in range(1,len(lista_extendida_max[0:7])):
                        data_atual=data_atual.replace(day=data_atual.day+1)
                        data_comp.append(data_atual.strftime("%d/%m/%y"))
                    print(f'Data_comp: {[data_comp[a] for a in range(0, len(data_comp))]}')
                    #executa a verificação se há info da cidade referente
                    for verificar_cidade in Prev_extendida.objects.all():
                        if verificar_cidade.cidade == data0:
                            cidade_count.append(verificar_cidade.cidade)
                            datas_cidade.append(verificar_cidade.data_prev)
                    #efetua a verificação se a data da previsão especifica consta no db
                    if len(cidade_count)>0 and datas_cidade!=data_comp:
                        for data in range(0,len(data_comp)):
                            if data_comp[data] not in datas_cidade:
                                print(data_comp[data])
                    if len(cidade_count)==0:
                        print('não há valores')
                        for a in range(0, len(data_comp)):
                            if data_comp[a]==data_comp[0]:
                                print(f'requisição do dia seguinte {data_comp[a]}')
                                cidade_info=Prev_extendida( 
                                    id_valores=id_cidade,
                                    cidade=data0,
                                    sigla=dados_0,
                                    max_diaria=maxima_list[1],
                                    min_diaria=minima_list[1],
                                    data_prev=data_comp[a]
                                )
                                cidade_info.save()
                            if data_comp[a]!=data_comp[0] and data_comp[a]!=data_comp[-1]:
                                print(f'requisição dos dias após o dia seguinte {data_comp[a]}')
                                cidade_info=Prev_extendida( 
                                    id_valores=id_cidade,
                                    cidade=data0,
                                    sigla=dados_0,
                                    max_diaria=lista_extendida_max[a-1],
                                    min_diaria=lista_extendida_min[a-1],
                                    data_prev=data_comp[a]
                                )
                                cidade_info.save()
                            if data_comp[a]==data_comp[-1]:
                                print(f'requisção do ultimo dia:{data_comp[a]}')
                                cidade_info=Prev_extendida( 
                                    id_valores=id_cidade,
                                    cidade=data0,
                                    sigla=dados_0,
                                    max_diaria=lista_extendida_max[a-1],
                                    min_diaria=lista_extendida_min[a-1],
                                    data_prev=data_comp[a]
                                )
                                cidade_info.save()
                                                    # if data_comp[a]==data_comp[0]:
                                                    #     dados_info=Prev_extendida(
                                                    #         id_valores=valor_id,
                                                    #         cidade=data0,
                                                    #         sigla=dados_0,
                                                    #         data_prev=data_comp[0],
                                                    #         max_diaria=maxima_list[1],
                                                    #         min_diaria=minima_list[1],
                                                    #     )
                                                    #     dados_info.save()
                                                    # if data_comp[a]!=data_comp[0] and data_comp[a]!=data_comp[-1]:
                                                    #     dados_info = Prev_extendida(
                                                    #         id_valores=valor_id,
                                                    #         cidade=data0,
                                                    #         data_prev=data_comp[a],
                                                    #         sigla=dados_0,
                                                    #         max_diaria=lista_extendida_max[a-1],
                                                    #         min_diaria=lista_extendida_min[a-1]
                                                    #     )
                                                    #     print(lista_extendida_max[a-1])
                                                    #     print(lista_extendida_min[a-1])
                                                    #     dados_info.save()
                                                    # if data_comp[a]==data_comp[-1]:
                                                    #     dados_info = Prev_extendida(
                                                    #         id_valores=valor_id,
                                                    #         cidade=data0,
                                                    #         data_prev=data_comp[-1],
                                                    #         sigla=dados_0,
                                                    #         max_diaria=lista_extendida_max[-2],
                                                    #         min_diaria=lista_extendida_min[-2]
                                                    #     )
                                                    #     dados_info.save()
                    if len(cidade_count)>0:
                        print(f'Dados da cidade{data0} já salvos')                     
                        
                for data_gerar_delete in Prev_extendida.objects.all():
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
                        sleep(2)
                        requisitar_prev()
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
                    sleep(2)
                    requisitar_prev()
                    return render(request, 'base.html', {'maxima':maxima_list[0], 'minima':minima_list[0]})
                
                print('Area de testes')
                print('requeste 200 sucesso')
    return render(request, 'base.html')