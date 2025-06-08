from rest_framework import serializers
from .models import Produto  # Ajuste o nome do modelo se for diferente

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'


