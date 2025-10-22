# utils.py - Refatorado para usar a estrutura de dados JSON em memória
from database import carregar_dados

def _buscar_entidade_por_id(nome_entidade, entidade_id):
    """Função auxiliar genérica para buscar um registro pelo ID."""
    
    # Garante que o ID seja tratado como inteiro para comparação com dados JSON
    try:
        entidade_id = int(entidade_id)
    except ValueError:
        return None
        
    dados = carregar_dados()
    
    # Busca o registro na lista correspondente, retornando None se não encontrar
    registro_encontrado = next((registro for registro in dados.get(nome_entidade, []) if registro.get('id') == entidade_id), None)
    
    return registro_encontrado

def buscar_cliente_por_id(cliente_id):
    """Busca cliente pelo ID"""
    return _buscar_entidade_por_id('clientes', cliente_id)

def buscar_carro_por_id(carro_id):
    """Busca carro pelo ID"""
    return _buscar_entidade_por_id('carros', carro_id)

def buscar_lavagem_por_id(lavagem_id):
    """Busca tipo de lavagem pelo ID"""
    return _buscar_entidade_por_id('tipos_lavagem', lavagem_id)

def listar_carros_por_cliente(cliente_id):
    """Lista todos os carros de um cliente"""
    try:
        cliente_id = int(cliente_id)
    except ValueError:
        return []
        
    dados = carregar_dados()
    
    # Filtra e retorna apenas os carros que pertencem ao cliente
    carros = [carro for carro in dados.get('carros', []) if carro.get('id_cliente') == cliente_id]
    
    return carros