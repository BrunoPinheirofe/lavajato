# clientes.py
from database import carregar_dados, salvar_dados
import re

def cadastrar_cliente():
    """Cadastra um novo cliente"""
    dados = carregar_dados()
    
    print("\n--- CADASTRO DE CLIENTE ---")
    nome = input("Nome: ").strip()
    telefone = input("Telefone: ").strip()
    email = input("E-mail: ").strip()
    
    # --- Validações ---
    if not nome:
        print("❌ Nome inválido!")
        print("Erro ao cadastrar o cliente.")
        return
    
    if not telefone :
        print("❌ Telefone inválido!")
        print("Erro ao cadastrar o cliente.")
        return
    
    # Validação simples de e-mail (pode usar regex)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("❌ E-mail inválido!")
        print("Erro ao cadastrar o cliente.")
        return
    
    # Verificar se o e-mail já está cadastrado
    for cliente_existente in dados['clientes']:
        if cliente_existente['email'].lower() == email.lower():
            print("❌ E-mail já cadastrado!")
            print("Erro ao cadastrar o cliente.")
            return
    
    # Gerar ID automático
    if dados['clientes']:
        novo_id = max(cliente['id'] for cliente in dados['clientes']) + 1
    else:
        novo_id = 1
    
    # Criar o dicionário do cliente
    cliente = {
        'id': novo_id,
        'nome': nome,
        'telefone': telefone,
        'email': email
    }
    
    # Salvar cliente
    dados['clientes'].append(cliente)
    salvar_dados(dados)
    print(f"✅ Cliente '{nome}' cadastrado com sucesso! ID: {novo_id}")
    
    # Perguntar se deseja cadastrar um carro
    opcao = input("Deseja cadastrar um carro para este cliente? (s/n): ").strip().lower()
    if opcao == 's':
        from carros import cadastrar_carro
        cadastrar_carro(novo_id)

def listar_clientes():
    """Lista todos os clientes"""
    dados = carregar_dados()
    
    print("\n--- LISTA DE CLIENTES ---")
    if not dados['clientes']:
        print("Nenhum cliente cadastrado.")
        return
    
    for cliente in dados['clientes']:
        print(f"ID: {cliente['id']} | Nome: {cliente['nome']} | Telefone: {cliente['telefone']} | E-mail: {cliente['email']}")
