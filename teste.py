# teste.py
from database import inicializar_arquivos, carregar_dados, salvar_dados

def popular_dados_teste():
    """Popula o sistema com dados de teste"""
    
    inicializar_arquivos()
    dados = carregar_dados()
    
    # Dados de exemplo
    dados['clientes'] = [
        {'id': 1, 'nome': 'Maria Santos', 'telefone': '11988888888', 'email': 'maria@email.com'},
        {'id': 2, 'nome': 'Pedro Oliveira', 'telefone': '11977777777', 'email': 'pedro@email.com'}
    ]
    
    dados['carros'] = [
        {'id': 1, 'id_cliente': 1, 'modelo': 'Honda Civic', 'placa': 'XYZ5678', 'cor': 'Prata'},
        {'id': 2, 'id_cliente': 2, 'modelo': 'Volkswagen Golf', 'placa': 'DEF9012', 'cor': 'Azul'}
    ]
    
    dados['tipos_lavagem'] = [
        {'id': 1, 'descricao': 'Lavagem Simples', 'preco': 25.00, 'tempo_medio': '30 minutos'},
        {'id': 2, 'descricao': 'Lavagem Completa', 'preco': 60.00, 'tempo_medio': '90 minutos'},
        {'id': 3, 'descricao': 'Lavagem Premium', 'preco': 120.00, 'tempo_medio': '120 minutos'}
    ]
    
    dados['agendamentos'] = [
        {'id': 1, 'id_cliente': 1, 'id_carro': 1, 'id_lavagem': 2, 'data': '20/12/2024', 'hora': '10:00', 'status': 'Agendado'},
        {'id': 2, 'id_cliente': 2, 'id_carro': 2, 'id_lavagem': 1, 'data': '21/12/2024', 'hora': '14:30', 'status': 'Confirmado'}
    ]
    
    salvar_dados(dados)
    print("✅ Dados de teste criados com sucesso!")
    print("📊 Resumo:")
    print(f"   👥 Clientes: {len(dados['clientes'])}")
    print(f"   🚗 Carros: {len(dados['carros'])}")
    print(f"   🧼 Tipos de Lavagem: {len(dados['tipos_lavagem'])}")
    print(f"   📅 Agendamentos: {len(dados['agendamentos'])}")

if __name__ == "__main__":
    popular_dados_teste()