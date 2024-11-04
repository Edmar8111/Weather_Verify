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