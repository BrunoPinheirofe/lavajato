# carros.py
from database import *
from utils import buscar_cliente_por_id

def cadastrar_carro_para_cliente(cliente_id, nome_cliente):
    """Cadastra carro para um cliente específico"""
    print(f"\n" + "="*50)
    print(f"CADASTRO DE CARRO PARA: {nome_cliente}")
    print("="*50)
    
    novo_id = gerar_novo_id(ARQUIVO_CARROS)
    modelo = input("Modelo do carro: ")
    marca = input("Marca: ")
    placa = input("Placa: ")
    ano = input("Ano: ")
    
    linha = f"{novo_id}|{cliente_id}|{modelo}|{marca}|{placa}|{ano}"
    escrever_linha(ARQUIVO_CARROS, linha)
    
    print(f"\nCarro '{modelo}' cadastrado com sucesso para {nome_cliente}! (ID: {novo_id})")

def cadastrar_carro():
    """Cadastra carro para cliente existente"""
    print("\n" + "="*50)
    print("CADASTRO DE CARRO")
    print("="*50)
    
    from clientes import listar_clientes
    listar_clientes()
    
    cliente_id = input("\nID do cliente: ")
    cliente = buscar_cliente_por_id(cliente_id)
    
    if not cliente:
        print("Cliente não encontrado!")
        return
    
    cadastrar_carro_para_cliente(cliente_id, cliente['nome'])

def listar_carros():
    """Lista todos os carros"""
    print("\n" + "="*50)
    print("CARROS CADASTRADOS")
    print("="*50)
    
    conteudo = ler_arquivo(ARQUIVO_CARROS)
    print(conteudo if conteudo else "Nenhum carro cadastrado ainda.")

def listar_carros_cliente(cliente_id=None):
    """Lista carros de um cliente específico"""
    from utils import buscar_cliente_por_id, listar_carros_por_cliente
    
    if cliente_id is None:
        cliente_id = input("ID do cliente: ")
    
    cliente = buscar_cliente_por_id(cliente_id)
    if not cliente:
        print("Cliente não encontrado!")
        return
    
    print(f"\n" + "="*50)
    print(f"CARROS DO CLIENTE: {cliente['nome']}")
    print("="*50)
    
    carros = listar_carros_por_cliente(cliente_id)
    if not carros:
        print("Nenhum carro cadastrado para este cliente.")
        return
    
    for carro in carros:
        print(f"ID: {carro['id']} - {carro['marca']} {carro['modelo']} - Placa: {carro['placa']} - Ano: {carro['ano']}")