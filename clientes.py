# clientes.py
from database import carregar_dados, salvar_dados

def cadastrar_cliente():
    """Cadastra um novo cliente"""
    dados = carregar_dados()
    
    print("\n--- CADASTRO DE CLIENTE ---")
    nome = input("Nome: ")
    telefone = input("Telefone: ")
    email = input("E-mail: ")
    
    # Gerar ID automático
    if dados['clientes']:
        novo_id = max(cliente['id'] for cliente in dados['clientes']) + 1
    else:
        novo_id = 1
    
    cliente = {
        'id': novo_id,
        'nome': nome,
        'telefone': telefone,
        'email': email
    }
    
    dados['clientes'].append(cliente)
    salvar_dados(dados)
    print(f"Cliente {nome} cadastrado com sucesso! ID: {novo_id}")
    
    # Perguntar se deseja cadastrar um carro
    if input("Deseja cadastrar um carro para este cliente? (s/n): ").lower() == 's':
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