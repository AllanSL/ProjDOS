from django.core.exceptions import ValidationError
from django.db import models

# Class Produto representa um produto no sistema de estoque
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_estoque = models.PositiveIntegerField()
    marca = models.CharField(max_length=16, null=False, blank=False)
    sku = models.CharField(max_length=16, unique=True, editable=False)

    def clean(self):
        if self.preco is None or self.preco == "":
            raise ValidationError({'preco': 'O preço não pode ser vazio.'})
        if self.saldo_estoque is None or self.saldo_estoque == "":
            raise ValidationError({'saldo_estoque': 'A quantidade em estoque não pode ser vazia.'})

        if float(self.preco) < 0:
            raise ValidationError({'preco': 'O preço não pode ser negativo.'})
        if int(self.saldo_estoque) < 0:
            raise ValidationError({'saldo_estoque': 'A quantidade em estoque não pode ser negativa.'})

    # Método para salvar o produto e gerar o SKU automaticamente
    def save(self, *args, **kwargs):
        # Chama o método clean() para validar os dados antes de salvar
        self.full_clean()
        if not self.sku:
            abreviacao_nome = ''.join(e for e in self.nome.upper() if e.isalnum())[:3]
            abreviacao_marca = ''.join(e for e in self.marca.upper() if e.isalnum())[:3]
            ultimo_id = Produto.objects.all().order_by('id').last()
            proximo_id = (ultimo_id.id + 1) if ultimo_id else 1
            # O SKU é gerado a partir da abreviação do nome e marca, seguido do ID do produto
            self.sku = f"{abreviacao_nome}{abreviacao_marca}-{str(proximo_id).zfill(9)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.sku})"
