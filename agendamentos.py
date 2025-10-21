# agendamentos.py
import json
from database import carregar_dados, salvar_dados

def cadastrar_agendamento():
    """Cadastra um novo agendamento de forma facilitada"""
    dados = carregar_dados()
    
    print("\n" + "=" * 50)
    print("📅 CADASTRO DE AGENDAMENTO")
    print("=" * 50)
    
    # Verificar se existem dados básicos
    if not dados['clientes']:
        print("❌ Nenhum cliente cadastrado. Cadastre um cliente primeiro.")
        return
    
    if not dados['carros']:
        print("❌ Nenhum carro cadastrado. Cadastre um carro primeiro.")
        return
    
    if not dados['tipos_lavagem']:
        print("❌ Nenhum tipo de lavagem cadastrado. Cadastre um tipo de lavagem primeiro.")
        return
    
    # PASSO 1: Selecionar Cliente
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
    
    # PASSO 2: Selecionar Carro do Cliente
    print(f"\n🚗 CARROS DO CLIENTE {cliente_selecionado['nome'].upper()}:")
    print("-" * 40)
    carros_cliente = [carro for carro in dados['carros'] if carro['id_cliente'] == id_cliente]
    
    if not carros_cliente:
        print("❌ Este cliente não possui carros cadastrados.")
        if input("Deseja cadastrar um carro agora? (s/n): ").lower() == 's':
            from carros import cadastrar_carro
            cadastrar_carro(id_cliente)
            # Recarregar dados após cadastro
            dados = carregar_dados()
            carros_cliente = [carro for carro in dados['carros'] if carro['id_cliente'] == id_cliente]
        else:
            return
    
    for carro in carros_cliente:
        print(f"ID: {carro['id']} | {carro['modelo']} | Placa: {carro['placa']} | Cor: {carro['cor']}")
    
    try:
        id_carro = int(input("\n📍 ID do carro: "))
        carro_selecionado = next((c for c in carros_cliente if c['id'] == id_carro), None)
        if not carro_selecionado:
            print("❌ Carro não encontrado ou não pertence ao cliente!")
            return
    except ValueError:
        print("❌ ID inválido!")
        return
    
    # PASSO 3: Selecionar Tipo de Lavagem (COM VALORES)
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
    
    # PASSO 4: Data e Hora
    print(f"\n📅 AGENDAMENTO PARA: {lavagem_selecionada['descricao']}")
    print(f"💵 VALOR: R$ {lavagem_selecionada['preco']:.2f}")
    print(f"⏰ TEMPO ESTIMADO: {lavagem_selecionada['tempo_medio']}")
    print("-" * 40)
    
    data_agendamento = input("Data (DD/MM/AAAA): ")
    hora_agendamento = input("Hora (HH:MM): ")
    
    # Confirmar agendamento
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
    if dados['agendamentos']:
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
    """Lista todos os agendamentos"""
    dados = carregar_dados()
    
    print("\n" + "=" * 60)
    print("📋 LISTA DE AGENDAMENTOS")
    print("=" * 60)
    
    if not dados['agendamentos']:
        print("📭 Nenhum agendamento cadastrado.")
        return
    
    for agendamento in dados['agendamentos']:
        # Encontrar informações relacionadas
        nome_cliente = "❌ Cliente não encontrado"
        for cliente in dados['clientes']:
            if cliente['id'] == agendamento['id_cliente']:
                nome_cliente = cliente['nome']
                break
        
        modelo_carro = "❌ Carro não encontrado"
        placa_carro = ""
        for carro in dados['carros']:
            if carro['id'] == agendamento['id_carro']:
                modelo_carro = carro['modelo']
                placa_carro = carro['placa']
                break
        
        descricao_lavagem = "❌ Lavagem não encontrada"
        preco_lavagem = 0.0
        for lavagem in dados['tipos_lavagem']:
            if lavagem['id'] == agendamento['id_lavagem']:
                descricao_lavagem = lavagem['descricao']
                preco_lavagem = lavagem['preco']
                break
        
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