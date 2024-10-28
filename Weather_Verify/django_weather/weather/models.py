from django.db import models
from datetime import datetime

# Create your models here.

class Info_clima_cidade(models.Model):
    nome_cidade = models.CharField(max_length=50, blank=False, default='Desconhecido')
    estado = models.CharField(max_length=10, default='desconhecido', blank=False)
    temp_max = models.IntegerField(default=0)
    temp_min = models.IntegerField(default=0)
    ind_uv = models.IntegerField(default=0)
    data_prev = models.DateTimeField(auto_now=True, editable=False)
    data_prev0 = models.CharField(max_length=50, default=str(datetime.now().strftime('%d/%m/%Y')))
