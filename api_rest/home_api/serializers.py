from rest_framework import serializers
from .models import valores

class valoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = valores
        fields = '__all__'
        #fields = ('nome_cidade', 'sigla_estado')