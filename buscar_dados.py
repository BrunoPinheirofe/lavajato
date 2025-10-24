
from database import carregar_dados

# --- FUNÇÕES DE BUSCA JSON  ---

def _buscar_entidade_por_id(nome_entidade, entidade_id):
    """Função auxiliar genérica para buscar um registro pelo ID."""
    try:
        entidade_id = int(entidade_id)
    except ValueError:
        return None
        
    dados = carregar_dados()
    
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
    
    carros = [carro for carro in dados.get('carros', []) if carro.get('id_cliente') == cliente_id]
    
    return carros