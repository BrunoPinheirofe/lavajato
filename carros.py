from database import carregar_dados, salvar_dados
from buscar_dados import buscar_cliente_por_id, listar_carros_por_cliente 

def _gerar_novo_id(lista_registros):
    """Função auxiliar para gerar novo ID baseado na lista."""
    if lista_registros:
        return max(registro['id'] for registro in lista_registros) + 1
    return 1

def cadastrar_carro_para_cliente(cliente_id, nome_cliente):
    """Cadastra carro para um cliente específico"""
    dados = carregar_dados()
    
    # Garante que cliente_id seja um inteiro para o formato JSON
    try:
        cliente_id_int = int(cliente_id)
    except ValueError:
        print("Erro: ID de cliente inválido.")
        return
    
    print(f"\n" + "="*50)
    print(f"CADASTRO DE CARRO PARA: {nome_cliente}")
    print("="*50)
    
    # Campos padronizados para o modelo JSON (modelo, placa, cor)
    modelo = input("Modelo do carro: ")
    placa = input("Placa: ")
    cor = input("Cor: ") 
    
    novo_id = _gerar_novo_id(dados['carros'])
    
    novo_carro = {
        'id': novo_id,
        'id_cliente': cliente_id_int,
        'modelo': modelo,
        'placa': placa,
        'cor': cor
    }
    
    dados['carros'].append(novo_carro)
    salvar_dados(dados)
    
    print(f"\nCarro '{modelo}' cadastrado com sucesso para {nome_cliente}! (ID: {novo_id})")

def cadastrar_carro():
    """Cadastra carro para cliente existente"""
    print("\n" + "="*50)
    print("CADASTRO DE CARRO")
    print("="*50)
    
    # A importação local de clientes.py é mantida para evitar dependência circular
    from clientes import listar_clientes
    listar_clientes()
    
    cliente_id_str = input("\nID do cliente: ")
    cliente = buscar_cliente_por_id(cliente_id_str) 
    
    if not cliente:
        print("Cliente não encontrado!")
        return
    
    cadastrar_carro_para_cliente(cliente_id_str, cliente['nome'])

def listar_carros():
    """Lista todos os carros"""
    dados = carregar_dados()
    
    print("\n" + "="*50)
    print("CARROS CADASTRADOS")
    print("="*50)
    
    if not dados['carros']:
        print("Nenhum carro cadastrado ainda.")
        return
        
    for carro in dados['carros']:
        # Busca o nome do cliente para exibição (usando a função de utils.py)
        cliente = buscar_cliente_por_id(carro['id_cliente'])
        nome_cliente = cliente['nome'] if cliente else "Cliente não encontrado"
        
        print(f"ID: {carro['id']} | Modelo: {carro['modelo']} | Placa: {carro['placa']} | Cor: {carro['cor']} | Cliente: {nome_cliente}")

def listar_carros_cliente(cliente_id=None):
    """Lista carros de um cliente específico"""
    # utils é importado acima
    
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
        print(f"ID: {carro['id']} - {carro['modelo']} - Placa: {carro['placa']} - Cor: {carro['cor']}")