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
prev_estendida = Prev_extendida.objects.all()
def home_0(request):
    valor_datas=[]
    msg_error = ''
    if request.method == 'POST': 
        
        #valor dos estados
        valor_cidades = (['Acre','AC'],['Alagoas','AL'],['Amapá','AP'],['Amazonas','AM'],
                     ['Bahia','BA'],['Ceará','CE'],['Distrito Federal','DF'],['Espírito Santo','ES']
                     ,['Goiás','GO'],['Maranhão','MA'],['Mato Grosso','MT'],['Mato Grosso do Sul','MS'],
                     ['Minas Gerais','MG'],['Pará','PA'],['Paraíba','PB'],['Paraná','PR'],['Pernambuco','PE'],
                     ['Piauí','PI'],['Rio de Janeiro','RJ'],['Rio Grande do Norte','RN'],['Rio Grande do Sul','RS'],
                     ['Rondônia','RO'],['Roraima','RR'],['Santa Catarina','SC'],['São Paulo','SP'],['Sergipe','SE'],['Tocantins','TO'])
        
        #requisição do front dos dados
        dados = str(request.POST['valor_0']).strip()
        data0 = str(request.POST['valor_1']).strip()
        
        #efetua a troca de valores com espaço por "_"
        if ' ' in data0:
            data0=str(data0).replace(' ', '_')
        
        #efetua a busca do estado referente
        for a in valor_cidades:
            if a[0] == dados:
                dados_0 = a[1]
        if dados_0 and len(data0)>0:
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
            
            #Efetua a verificação do valor de estado
            for recorte_texto in valor_target:
                valor_target0 = str(recorte_texto.text[10:13]).strip()
            for recorte_texto0 in valor_target:
                cidade_raspagem = str(recorte_texto0.text[:len(data0)]).strip()     
            
            #Efetua o save dos dados
            for a in valor_target_maxima:
                maxima_list.append(a.text[0:2])
            for a in valor_target_minima:
                minima_list.append(a.text[0:2])
            for a in valor_target_prev:
                lista_extendida_min.append(str(a.text[0:2])) 
            for a in valor_target_prev_0:
                lista_extendida_max.append(str(a.text[0:2]))
            
            #efetua a requiseção de cidade não existente
            if valor_target0 == 'DF' or data0=='':
                #efetua a requiseção de cidade não existente
                 msg_error = 'Valor da Cidade Incorreta'       
                 return render(request, 'base.html', {'msg_error':msg_error})
            
            else:
                #efetua a exclusão de dados sem info
                for data_gerar_delete in Prev_extendida.objects.all():
                       if data_gerar_delete.cidade=='desconhecida' or data_gerar_delete.max_diaria==0:
                           data_gerar_delete.delete()
               
                def requisitar_prev():
                    import datetime
                    data_atual = datetime.datetime.today()
                    data_comp=[]
                    cidade_count=[]
                    datas_cidade=[]
                    datas_faltantes=[]
                    id_cidade=0
                    for a in Prev_extendida.objects.all():
                        Prev_extendida.objects.get(pk=a.id).delete()
                    #efetua a requisição do id da cidade referente no banco de dados
                    for id_cidade_0 in valores.objects.all():
                        if id_cidade_0.nome_cidade==cidade_raspagem:
                            id_cidade=id_cidade_0.id
                    
                    #autenticação de data e implementação na lista
                    for data_0 in range(1,len(lista_extendida_max[0:7])):
                        data_atual=data_atual.replace(day=data_atual.day+1)
                        data_comp.append(data_atual.strftime("%d/%m/%y"))
                    
                    #executa a verificação se há info da cidade referente
                    for verificar_cidade in Prev_extendida.objects.all():
                        if verificar_cidade.cidade == cidade_raspagem:
                            cidade_count.append(verificar_cidade.cidade)
                            datas_cidade.append(verificar_cidade.data_prev)
              
                    #efetua a verificação se a data da previsão especifica consta no db
                    if len(cidade_count)>0 and datas_cidade!=data_comp:
                        for data in range(0,len(data_comp)):
                            if data_comp[data] not in datas_cidade:
                                datas_faltantes.append(data_comp[data])
                        sleep(0.5)
                    
                    #caso haja valores obsoletos de datas, eles serão sobrepostos
                    if len(datas_faltantes)>0:    
                        valores.objects.get(pk=id_cidade).delete()
                        cidade_count=[]       
                    sleep(0.5)
                    
                    #Efetua o save dos dados caso não constem no db    
                    if len(cidade_count)==0:
                        print('não há valores')
                        for a in range(0, len(data_comp)):
                            if data_comp[a]==data_comp[0]:
                                print(f'requisição do dia seguinte {data_comp[a]}')
                                cidade_info=Prev_extendida( 
                                    id_valores=id_cidade,
                                    cidade=cidade_raspagem,
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
                                    cidade=cidade_raspagem,
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
                                    cidade=cidade_raspagem,
                                    sigla=dados_0,
                                    max_diaria=lista_extendida_max[-2],
                                    min_diaria=lista_extendida_min[-2],
                                    data_prev=data_comp[a]
                                )
                                cidade_info.save()
                    
                    #Executa a verificação das datas que constam no db
                    for dados_anteriores in Prev_extendida.objects.all():
                            if dados_anteriores.id_valores==id_cidade:
                                valor_datas.append(dados_anteriores.id)
                    
                #executa a parte inicial da requisição
                from time import sleep
                validar_exec = 0

                #Executa a exclusão de arquivos que não possuem info
                for a in valores.objects.all():
                    if a.nome_cidade == 'desconhecida' or a.maxima==0:
                        a.delete()
                
                #Efetua a busca dos dados dentro do db
                for a in valores.objects.all():
                    if cidade_raspagem == a.nome_cidade and dados_0 == a.sigla_estado:
                        dados = valores.objects.get(pk=a.id)
                        validar_exec=+1
                        requisitar_prev()
                        return render(request,'base.html', {
                            'maxima':dados.maxima, 'minima':dados.minima, 'sigla':dados.sigla_estado, 'cidade':dados.nome_cidade.upper,
                            'dia_0':Prev_extendida.objects.get(pk=int(valor_datas[-6])),
                            'dia_1':Prev_extendida.objects.get(pk=int(valor_datas[-5])),
                            'dia_2':Prev_extendida.objects.get(pk=int(valor_datas[-4])),
                            'dia_3':Prev_extendida.objects.get(pk=int(valor_datas[-3])),
                            'dia_4':Prev_extendida.objects.get(pk=int(valor_datas[-2])),
                            'dia_5':Prev_extendida.objects.get(pk=int(valor_datas[-1]))
                            })
                    
                #efetua a requisição dos dados caso não constem no banco de dados
                sleep(5)
                if validar_exec==0:
                    db_request_save = valores(
                        nome_cidade=str(cidade_raspagem),
                        sigla_estado=str(dados_0),
                        maxima=int(maxima_list[0]),
                        minima=int(minima_list[0]),
                        )
                    db_request_save.save()
                    sleep(2)
                    requisitar_prev()
                    sleep(2)
                    return render(request, 'base.html', {'maxima':maxima_list[0], 'minima':minima_list[0], 'sigla':str(dados_0).upper,'cidade':str(cidade_raspagem).upper,
                            'dia_0':Prev_extendida.objects.get(pk=int(valor_datas[-6])),
                            'dia_1':Prev_extendida.objects.get(pk=int(valor_datas[-5])),
                            'dia_2':Prev_extendida.objects.get(pk=int(valor_datas[-4])),
                            'dia_3':Prev_extendida.objects.get(pk=int(valor_datas[-3])),
                            'dia_4':Prev_extendida.objects.get(pk=int(valor_datas[-2])),
                            'dia_5':Prev_extendida.objects.get(pk=int(valor_datas[-1]))                             
                            })
        
        else:
            msg_error = 'Valor da Cidade Incorreta'       
            return render(request, 'base.html', {'msg_error':msg_error})
    if request.method=='GET':
        return render(request, 'base.html')