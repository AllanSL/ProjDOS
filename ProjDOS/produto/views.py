from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Produto
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from decimal import Decimal, ROUND_DOWN
from django.contrib.auth.views import LoginView

def is_superuser(user):
    return user.is_superuser

@login_required(login_url=reverse_lazy('login'))
def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produto/listar_produtos.html', {'produtos': produtos})

@user_passes_test(is_superuser, login_url=reverse_lazy('listar_produtos'))
@login_required(login_url=reverse_lazy('login'))
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == 'POST':
        try:
            # Remove a formatação monetária do campo 'preco'
            preco = request.POST.get('preco', '').replace("R$", "").replace(".", "").replace(",", ".").strip()
            saldo_estoque = request.POST.get('saldo_estoque', '').strip()

            # Validações adicionais
            if not preco or float(preco) < 0:
                messages.error(request, 'O preço não pode ser vazio ou menor que zero.')
                return render(request, 'produto/editar_produto.html', {'produto': produto})

            if not saldo_estoque or int(saldo_estoque) < 0:
                messages.error(request, 'A quantidade em estoque não pode ser vazia ou negativa.')
                return render(request, 'produto/editar_produto.html', {'produto': produto})

            # Arredonda o preço para no máximo 2 casas decimais
            preco = Decimal(preco).quantize(Decimal('0.01'), rounding=ROUND_DOWN)

            # Atualiza o produto
            produto.preco = preco
            produto.saldo_estoque = int(saldo_estoque)
            produto.descricao = request.POST.get('descricao', '').strip()
            produto.full_clean()  # Valida os dados
            produto.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('listar_produtos')
        except ValueError:
            messages.error(request, 'Erro ao processar os valores. Verifique os campos preenchidos.')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    return render(request, 'produto/editar_produto.html', {'produto': produto})

@user_passes_test(is_superuser, login_url=reverse_lazy('listar_produtos'))
@login_required(login_url=reverse_lazy('login'))
def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('listar_produtos')

@user_passes_test(is_superuser, login_url=reverse_lazy('listar_produtos'))
@login_required(login_url=reverse_lazy('login'))
def criar_produto(request):
    if request.method == 'POST':
        try:
            preco_raw = request.POST.get('preco', '')
            saldo_estoque_raw = request.POST.get('saldo_estoque', '')

            if not preco_raw or not saldo_estoque_raw:
                messages.error(request, 'Preencha todos os campos obrigatórios.')
                return render(request, 'produto/criar_produto.html')

            preco = Decimal(preco_raw.replace("R$", "").replace(".", "").replace(",", ".").strip()).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
            saldo_estoque = int(saldo_estoque_raw.strip())

            try:
                Produto.objects.create(
                    nome=request.POST.get('nome', '').strip(),
                    descricao=request.POST.get('descricao', '').strip(),
                    marca=request.POST.get('marca', '').strip(),
                    preco=preco,
                    saldo_estoque=saldo_estoque,
                )
                messages.success(request, 'Produto criado com sucesso!')
                return redirect('listar_produtos')
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except ValueError:
            messages.error(request, 'Erro ao processar os valores. Verifique os campos preenchidos.')

    return render(request, 'produto/criar_produto.html')

class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('listar_produtos')  # ou a URL que desejar
        return super().dispatch(request, *args, **kwargs)
