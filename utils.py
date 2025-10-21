# utils.py
from database import *
from sistema_lava_jato import ARQUIVO_AGENDAMENTOS,ARQUIVO_CARROS,ARQUIVO_CLIENTES,ARQUIVO_LAVAGENS

def buscar_cliente_por_id(cliente_id):
    """Busca cliente pelo ID"""
    try:
        with open('clientes.json', 'r', encoding='utf-8') as f:
            for linha in f.readlines()[1:]:
                dados = linha.strip().split('|')
                if dados[0] == cliente_id:
                    return {'id': dados[0], 'nome': dados[1], 'telefone': dados[2], 'email': dados[3]}
    except:
        return None

def buscar_carro_por_id(carro_id):
    """Busca carro pelo ID"""
    try:
        with open(ARQUIVO_CARROS, 'r', encoding='utf-8') as f:
            for linha in f.readlines()[1:]:
                dados = linha.strip().split('|')
                if dados[0] == carro_id:
                    return {'id': dados[0], 'cliente_id': dados[1], 'modelo': dados[2], 'marca': dados[3], 'placa': dados[4], 'ano': dados[5]}
    except:
        return None

def buscar_lavagem_por_id(lavagem_id):
    """Busca tipo de lavagem pelo ID"""
    try:
        with open(ARQUIVO_LAVAGENS, 'r', encoding='utf-8') as f:
            for linha in f.readlines()[1:]:
                dados = linha.strip().split('|')
                if dados[0] == lavagem_id:
                    return {'id': dados[0], 'tipo': dados[1], 'descricao': dados[2], 'preco': dados[3], 'tempo': dados[4]}
    except:
        return None

def listar_carros_por_cliente(cliente_id):
    """Lista todos os carros de um cliente"""
    carros = []
    try:
        with open(ARQUIVO_CARROS, 'r', encoding='utf-8') as f:
            for linha in f.readlines()[1:]:
                dados = linha.strip().split('|')
                if dados[1] == cliente_id:
                    carros.append({'id': dados[0], 'modelo': dados[2], 'marca': dados[3], 'placa': dados[4], 'ano': dados[5]})
    except:
        pass
    return carros