# remover.py
from database import carregar_dados, salvar_dados
from validadores import ler_id_valido
# Importa listar_clientes/carros/etc para exibir as opções
from clientes import listar_clientes
from carros import listar_carros
from lavagens import listar_tipos_lavagem
from agendamentos import listar_agendamentos

def remover_registro():
    """Função universal para remover qualquer tipo de registro"""
    
    print("\n" + "=" * 50)
    print("REMOVER REGISTRO - SISTEMA LAVA JATO")
    print("=" * 50)
    print("1. Remover Cliente")
    print("2. Remover Carro")
    print("3. Remover Tipo de Lavagem")
    print("4. Remover Agendamento")
    print("5. Voltar")
    print("-" * 50)
    
    opcao = input("Escolha o tipo de registro a remover: ")
    
    if opcao == '1':
        _remover_entidade('clientes', 'Cliente', listar_clientes, True) # O True indica que a remoção é complexa (dependências)
    elif opcao == '2':
        _remover_entidade('carros', 'Carro', listar_carros, False)
    elif opcao == '3':
        _remover_entidade('tipos_lavagem', 'Tipo de Lavagem', listar_tipos_lavagem, False)
    elif opcao == '4':
        _remover_entidade('agendamentos', 'Agendamento', listar_agendamentos, False)
    elif opcao == '5':
        return
    else:
        print("Opção inválida!")

def _remover_entidade(nome_entidade, nome_exibicao, funcao_listar, checar_dependencias):
    """Função auxiliar para remover uma entidade específica"""
    
    dados = carregar_dados()
    
    print(f"\n--- REMOVER {nome_exibicao.upper()} ---")
    
    # 1. Listar registros existentes
    if not dados[nome_entidade]:
        print(f"Nenhum {nome_exibicao.lower()} cadastrado para remover.")
        return
    
    # Chama a função de listagem do módulo específico (clientes.py, carros.py, etc.)
    funcao_listar() 
    
    id_registro = ler_id_valido(f"\nID do {nome_exibicao.lower()} a remover: ")
    
    # Encontrar o índice do registro
    indice_remocao = -1
    for i, registro in enumerate(dados[nome_entidade]):
        if registro['id'] == id_registro:
            indice_remocao = i
            break
            
    if indice_remocao == -1:
        print(f"❌ {nome_exibicao} com ID {id_registro} não encontrado!")
        return

    # 2. Checagem de dependências (Apenas para Cliente)
    if checar_dependencias:
        carros_vinculados = [c for c in dados['carros'] if c['id_cliente'] == id_registro]
        agendamentos_vinculados = [a for a in dados['agendamentos'] if a['id_cliente'] == id_registro]
        
        if carros_vinculados or agendamentos_vinculados:
            print("\n⚠️ ALERTA DE DEPENDÊNCIAS!")
            print(f"Este cliente possui {len(carros_vinculados)} carro(s) e {len(agendamentos_vinculados)} agendamento(s) vinculados.")
            
            confirmar_remocao_total = input("Deseja realmente remover o cliente E TODOS os seus dados vinculados? (s/n): ").lower()
            
            if confirmar_remocao_total != 's':
                print(f"❌ Remoção de {nome_exibicao} cancelada.")
                return
            
            # Remove carros e agendamentos vinculados
            dados['carros'] = [c for c in dados['carros'] if c['id_cliente'] != id_registro]
            dados['agendamentos'] = [a for a in dados['agendamentos'] if a['id_cliente'] != id_registro]

    # 3. Confirmação e Remoção
    confirmar = input(f"Tem certeza que deseja remover o {nome_exibicao.lower()} ID {id_registro}? (s/n): ").lower()
    
    if confirmar == 's':
        del dados[nome_entidade][indice_remocao]
        salvar_dados(dados)
        print(f"✅ {nome_exibicao} ID {id_registro} removido com sucesso!")
    else:
        print(f"❌ Remoção de {nome_exibicao} cancelada.")