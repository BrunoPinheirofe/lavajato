# database.py
import json
import os

def inicializar_arquivos():
    """Inicializa os arquivos JSON se não existirem"""
    arquivos = ['clientes.json', 'carros.json', 'tipos_lavagem.json', 'agendamentos.json']
    
    for arquivo in arquivos:
        if not os.path.exists(arquivo):
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

def carregar_dados():
    """Carrega todos os dados dos arquivos JSON"""
    dados = {}
    
    try:
        with open('clientes.json', 'r', encoding='utf-8') as f:
            dados['clientes'] = json.load(f)
    except:
        dados['clientes'] = []
    
    try:
        with open('carros.json', 'r', encoding='utf-8') as f:
            dados['carros'] = json.load(f)
    except:
        dados['carros'] = []
    
    try:
        with open('tipos_lavagem.json', 'r', encoding='utf-8') as f:
            dados['tipos_lavagem'] = json.load(f)
    except:
        dados['tipos_lavagem'] = []
    
    try:
        with open('agendamentos.json', 'r', encoding='utf-8') as f:
            dados['agendamentos'] = json.load(f)
    except:
        dados['agendamentos'] = []
    
    return dados

def salvar_dados(dados):
    """Salva todos os dados nos arquivos JSON"""
    with open('clientes.json', 'w', encoding='utf-8') as f:
        json.dump(dados['clientes'], f, ensure_ascii=False, indent=2)
    
    with open('carros.json', 'w', encoding='utf-8') as f:
        json.dump(dados['carros'], f, ensure_ascii=False, indent=2)
    
    with open('tipos_lavagem.json', 'w', encoding='utf-8') as f:
        json.dump(dados['tipos_lavagem'], f, ensure_ascii=False, indent=2)
    
    with open('agendamentos.json', 'w', encoding='utf-8') as f:
        json.dump(dados['agendamentos'], f, ensure_ascii=False, indent=2)