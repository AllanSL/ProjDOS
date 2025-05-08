# ProjDOS - Módulo de Produto

Este repositório contém o módulo de **Produto** do sistema **ProjDOS**, desenvolvido com Django e Bootstrap. Ele permite o gerenciamento de produtos com funcionalidades completas de CRUD (Create, Read, Update, Delete) e autenticação de acesso.

## ⚙️ Funcionalidades

- Cadastro de novos produtos
- Edição e exclusão de produtos existentes
- Listagem de produtos em tabela interativa
- Detalhamento individual via modais
- Geração automática de SKU com base no nome, marca e ID
- Sistema de login com autenticação obrigatória para todas as funcionalidades
- Modais personalizados para confirmação de exclusão e logout
- Interface responsiva com Bootstrap 5
- Mensagens de sucesso e feedback para o usuário
- Tabela com paginação, busca e ordenação usando DataTables

## 🧱 Estrutura dos Dados

O modelo `Produto` possui os seguintes campos:

| Campo          | Tipo                   | Descrição                                               |
|----------------|------------------------|----------------------------------------------------------|
| `nome`         | `CharField` (max=100)  | Nome do produto                                          |
| `descricao`    | `TextField`            | Descrição do produto (opcional)                          |
| `preco`        | `DecimalField`         | Preço do produto (até 10 dígitos, 2 casas decimais)      |
| `saldo_estoque`| `PositiveIntegerField` | Quantidade em estoque                                    |
| `marca`        | `CharField` (max=16)   | Nome da marca (salvo em caixa alta, até 16 caracteres)   |
| `sku`          | `CharField` (max=16)   | Código único gerado automaticamente e não editável       |

### Geração de SKU

O SKU é criado automaticamente com base em:
- 3 primeiras letras do nome (sem acentos e símbolos)
- 3 primeiras letras da marca
- ID do produto com 9 dígitos (com zero à esquerda)

**Exemplo:** `CAFNES-000000015`

---

## 🔐 Autenticação

Todas as rotas são protegidas com `@login_required`. O acesso ao sistema exige login com credenciais de superusuário.

## 💡 Requisitos

- Python 3.10+
- Django 4.x
- Bootstrap 5.3.6
- jQuery e DataTables

## 🧪 Instalação e Execução

1. Clone o projeto:
   ```bash
   git clone https://github.com/seu-usuario/ProjDOS.git
   cd ProjDOS
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install django
   ```

4. Aplique as migrações:
   ```bash
   python manage.py migrate
   ```

5. Crie um superusuário:
   ```bash
   python manage.py createsuperuser
   ```

6. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

7. Acesse:
   ```
   http://localhost:8000/
   ```

## 👨‍💻 Desenvolvido por

- Allan Batista
- Luan da Silva
- Samylla Marinho

5º Período – Curso de Análise e Desenvolvimento de Sistemas  
Instituto Federal do Tocantins – Campus Araguaína
