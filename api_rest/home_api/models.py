from django.db import models

# Create your models here.

class valores(models.Model):
    class Meta:
        db_table = 'valores'
    nome_cidade = models.CharField(default='desconhecida', max_length=100)
    sigla_estado = models.CharField(default='desconhecida', max_length=100)
    data_previsao = models.DateTimeField(auto_now=True)
    maxima = models.IntegerField(default=0)
    minima = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nome_cidade, self.sigla_estado
class Prev_extendida(models.Model):
    id_valores=models.IntegerField(default=0, blank=None)
    cidade=models.CharField(default='desconhecida', max_length=100)
    sigla=models.CharField(default='desconhecida', max_length=50)
    data_prev=models.CharField(default='00/00/00', max_length=50)
    max_diaria=models.IntegerField(default=0)
    min_diaria=models.IntegerField(default=0)