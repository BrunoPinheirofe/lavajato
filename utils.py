
from database import carregar_dados


def ler_id_valido(prompt):
    """Lê um input e garante que seja um ID (inteiro positivo)."""
    while True:
        try:
            valor = input(prompt)
            id_int = int(valor)
            if id_int > 0:
                return id_int
            else:
                print("ID deve ser um número positivo. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

def ler_float_valido(prompt):
    """Lê um input e garante que seja um valor numérico válido (float)."""
    while True:
        try:
            # Substitui vírgula por ponto e remove 'R$' para facilitar a conversão
            valor = input(prompt).replace('R$', '').replace(',', '.').strip()
            if not valor:
                return None # Permite que o usuário deixe em branco na edição
            return float(valor)
        except ValueError:
            print("Entrada inválida. Digite um valor numérico válido.")

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