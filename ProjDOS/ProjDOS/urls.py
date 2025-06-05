from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from produto import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.CustomLoginView.as_view(), name='login'),  # tela de login como página inicial
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('produtos/', views.listar_produtos, name='listar_produtos'),
    path('produtos/editar/', lambda request: redirect('listar_produtos'), name='editar_produto_sem_id'),
    path('produtos/editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),
    path('produtos/excluir/', lambda request: redirect('listar_produtos'), name='excluir_produto_sem_id'),
    path('produtos/excluir/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),
    path('produtos/criar/', views.criar_produto, name='criar_produto'),
]
