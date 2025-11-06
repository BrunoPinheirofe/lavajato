

import json
from database import carregar_dados, salvar_dados
from datetime import datetime # Importa o módulo datetime
from buscar_dados import buscar_cliente_por_id, buscar_carro_por_id, buscar_lavagem_por_id


def cadastrar_agendamento():
    """Cadastra um novo agendamento de forma facilitada"""
    dados = carregar_dados()
    
    print("\n" + "=" * 50)
    print("📅 CADASTRO DE AGENDAMENTO")
    print("=" * 50)
    
    # ----------------------------------------------------
    # PASSO 1: Selecionar Cliente
    if not dados.get('clientes'):
        print("❌ Nenhum cliente cadastrado. Cadastre um cliente primeiro.")
        return
        
    print("\n👥 SELECIONE O CLIENTE:")
    print("-" * 30)
    for cliente in dados['clientes']:
        print(f"ID: {cliente['id']} | {cliente['nome']}")
    
    try:
        id_cliente = int(input("\n📍 ID do cliente: "))
        cliente_selecionado = next((c for c in dados['clientes'] if c['id'] == id_cliente), None)
        if not cliente_selecionado:
            print("❌ Cliente não encontrado!")
            return
    except ValueError:
        print("❌ ID inválido!")
        return

    # ----------------------------------------------------
    
    print(f"\n🚗 CARROS DO CLIENTE {cliente_selecionado['nome'].upper()}:")
    print("-" * 40)
    carros_cliente = [carro for carro in dados.get('carros', []) if carro.get('id_cliente') == id_cliente]
    
    if not carros_cliente:
        print("❌ Este cliente não possui carros cadastrados.")
        if input("Deseja cadastrar um carro agora? (s/n): ").lower() == 's':
            from carros import cadastrar_carro_para_cliente
            cadastrar_carro_para_cliente(id_cliente, cliente_selecionado['nome'])
            # Recarregar dados após cadastro
            dados = carregar_dados()
            carros_cliente = [carro for carro in dados.get('carros', []) if carro.get('id_cliente') == id_cliente]
            if not carros_cliente: return # Sai se o carro ainda não foi cadastrado
        else:
            return
    
    for carro in carros_cliente:
        print(f"ID: {carro['id']} | {carro['modelo']} | Placa: {carro['placa']} | Cor: {carro.get('cor', 'N/A')}")
    
    try:
        id_carro = int(input("\n📍 ID do carro: "))
        carro_selecionado = next((c for c in carros_cliente if c['id'] == id_carro), None)
        if not carro_selecionado:
            print("❌ Carro não encontrado ou não pertence ao cliente!")
            return
    except ValueError:
        print("❌ ID inválido!")
        return
    
    # ----------------------------------------------------
    
    if not dados.get('tipos_lavagem'):
        print("❌ Nenhum tipo de lavagem cadastrado. Cadastre um tipo de lavagem primeiro.")
        return
        
    print(f"\n🧼 TIPOS DE LAVAGEM DISPONÍVEIS:")
    print("=" * 50)
    for lavagem in dados['tipos_lavagem']:
        print(f"ID: {lavagem['id']} | {lavagem['descricao']:20} | R$ {lavagem['preco']:6.2f} | ⏱️  {lavagem['tempo_medio']}")
    print("=" * 50)
    
    try:
        id_lavagem = int(input("\n📍 ID do tipo de lavagem: "))
        lavagem_selecionada = next((l for l in dados['tipos_lavagem'] if l['id'] == id_lavagem), None)
        if not lavagem_selecionada:
            print("❌ Tipo de lavagem não encontrado!")
            return
    except ValueError:
        print("❌ ID inválido!")
        return
    
    # ----------------------------------------------------
    print(f"\n📅 AGENDAMENTO PARA: {lavagem_selecionada['descricao']}")
    print(f"💵 VALOR: R$ {lavagem_selecionada['preco']:.2f}")
    print(f"⏰ TEMPO ESTIMADO: {lavagem_selecionada['tempo_medio']}")
    print("-" * 40)
    
    data_hora_valida = False
    data_agendamento = ""
    hora_agendamento = ""
    
    while not data_hora_valida:
        data_input = input("Data (DD/MM/AAAA): ")
        hora_input = input("Hora (HH:MM): ")
        
        data_hora_str = f"{data_input} {hora_input}"
        
        try:
            # Tenta converter a string para um objeto datetime
            agendamento_dt = datetime.strptime(data_hora_str, '%d/%m/%Y %H:%M')
            
            # 1. Checa se o agendamento está no futuro
            if agendamento_dt < datetime.now():
                print("❌ Não é possível agendar em uma data/hora que já passou. Tente novamente.")
                continue
                
            # As datas e horas validadas
            data_agendamento = data_input
            hora_agendamento = hora_input
            data_hora_valida = True
            
        except ValueError:
            print("❌ Formato de data ou hora inválido. Use DD/MM/AAAA e HH:MM. Tente novamente.")

    
    # ----------------------------------------------------
    
    print(f"\n✅ RESUMO DO AGENDAMENTO:")
    print(f"   👤 Cliente: {cliente_selecionado['nome']}")
    print(f"   🚗 Carro: {carro_selecionado['modelo']} - {carro_selecionado['placa']}")
    print(f"   🧼 Serviço: {lavagem_selecionada['descricao']}")
    print(f"   💵 Valor: R$ {lavagem_selecionada['preco']:.2f}")
    print(f"   📅 Data: {data_agendamento} às {hora_agendamento}")
    
    confirmar = input("\nConfirmar agendamento? (s/n): ").lower()
    
    if confirmar != 's':
        print("❌ Agendamento cancelado.")
        return
    
    # Gerar ID automático
    if dados.get('agendamentos'):
        novo_id = max(agendamento['id'] for agendamento in dados['agendamentos']) + 1
    else:
        novo_id = 1
    
    agendamento = {
        'id': novo_id,
        'id_cliente': id_cliente,
        'id_carro': id_carro,
        'id_lavagem': id_lavagem,
        'data': data_agendamento,
        'hora': hora_agendamento,
        'status': 'Agendado'
    }
    
    dados['agendamentos'].append(agendamento)
    salvar_dados(dados)
    
    print(f"\n🎉 AGENDAMENTO CONCLUÍDO COM SUCESSO!")
    print(f"📋 Número do agendamento: {novo_id}")
    print(f"📞 Cliente: {cliente_selecionado['nome']} - {cliente_selecionado['telefone']}")


def listar_agendamentos():
    
    dados = carregar_dados()
    
    print("\n" + "=" * 60)
    print("📋 LISTA DE AGENDAMENTOS")
    print("=" * 60)
    
    if not dados.get('agendamentos'):
        print("📭 Nenhum agendamento cadastrado.")
        return
    
    for agendamento in dados['agendamentos']:
        # Encontrar informações relacionadas (Busca Modular)
        cliente = buscar_cliente_por_id(agendamento['id_cliente'])
        nome_cliente = cliente['nome'] if cliente else "❌ Cliente não encontrado"

        carro = buscar_carro_por_id(agendamento['id_carro'])
        modelo_carro = carro.get('modelo', '❌ Carro não encontrado')
        placa_carro = carro.get('placa', 'N/A')

        # USAMOS A BUSCA MODULAR PARA LAVAGEM, REMOVENDO O LOOP MANUAL
        lavagem = buscar_lavagem_por_id(agendamento['id_lavagem'])
        descricao_lavagem = lavagem.get('descricao', '❌ Lavagem não encontrada')
        preco_lavagem = lavagem.get('preco', 0.0)
        
        # Emojis para status
        emoji_status = {
            'Agendado': '📅',
            'Confirmado': '✅',
            'Em Andamento': '🔄',
            'Concluído': '🎉',
            'Cancelado': '❌'
        }
        
        status_emoji = emoji_status.get(agendamento['status'], '📝')
        
        print(f"#{agendamento['id']} {status_emoji} {agendamento['status']}")
        print(f"   👤 {nome_cliente}")
        print(f"   🚗 {modelo_carro} - {placa_carro}")
        print(f"   🧼 {descricao_lavagem} - R$ {preco_lavagem:.2f}")
        print(f"   📅 {agendamento['data']} às {agendamento['hora']}")
        print("-" * 60)