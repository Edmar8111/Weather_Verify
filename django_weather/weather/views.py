from django.shortcuts import render,HttpResponse

# Create your views here.

def home(request):
    return render(request, "base.html")

def testes():
    dict_cidades = {'cidade':'sigla', 'cidade':'sigla'}
    for a in dict_cidades:
        print(a)