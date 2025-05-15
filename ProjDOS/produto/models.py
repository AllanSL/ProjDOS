from django.db import models

# Class Produto representa um produto no sistema de estoque
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_estoque = models.PositiveIntegerField()
    marca = models.CharField(max_length=16, null=False, blank=False)
    sku = models.CharField(max_length=16, unique=True, editable=False)

    # Método para salvar o produto e gerar o SKU automaticamente
    def save(self, *args, **kwargs):
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
