from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Produto
from django.contrib import messages

@login_required(login_url=reverse_lazy('login'))
def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produto/listar_produtos.html', {'produtos': produtos})

@login_required(login_url=reverse_lazy('login'))
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == 'POST':
        # Atualiza os campos do produto com os dados do formulário
        produto.nome = request.POST.get('nome')
        produto.sku = request.POST.get('sku')
        produto.marca = request.POST.get('marca')
        produto.preco = request.POST.get('preco')
        produto.saldo_estoque = request.POST.get('saldo_estoque')
        produto.descricao = request.POST.get('descricao')
        produto.save()
        messages.success(request, 'Produto atualizado com sucesso!')
        return redirect('listar_produtos')

    return render(request, 'produto/editar_produto.html', {'produto': produto})

@login_required(login_url=reverse_lazy('login'))
def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('listar_produtos')

@login_required(login_url=reverse_lazy('login'))
def criar_produto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        saldo_estoque = request.POST.get('saldo_estoque')
        marca = request.POST.get('marca')

        produto = Produto(
            nome=nome,
            descricao=descricao,
            preco=preco,
            saldo_estoque=saldo_estoque,
            marca=marca.upper()[:16] if marca else "",
        )
        produto.save()
        messages.success(request, 'Produto criado com sucesso!')
        return redirect('listar_produtos')
    
    return render(request, 'produto/criar_produto.html')
