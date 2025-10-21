# editar.py
from database import carregar_dados, salvar_dados

def editar_registro():
    """Função universal para editar qualquer tipo de registro"""
    
    dados = carregar_dados()
    
    print("\n" + "=" * 50)
    print("EDITAR REGISTRO - SISTEMA LAVA JATO")
    print("=" * 50)
    print("1. Editar Cliente")
    print("2. Editar Carro")
    print("3. Editar Tipo de Lavagem")
    print("4. Editar Agendamento")
    print("5. Voltar")
    print("-" * 50)
    
    opcao = input("Escolha o tipo de registro: ")
    
    if opcao == '1':
        _editar_entidade(dados, 'clientes', 'Cliente', ['nome', 'telefone', 'email'])
    elif opcao == '2':
        _editar_entidade(dados, 'carros', 'Carro', ['modelo', 'placa', 'cor'])
    elif opcao == '3':
        _editar_entidade(dados, 'tipos_lavagem', 'Tipo de Lavagem', ['descricao', 'preco', 'tempo_medio'])
    elif opcao == '4':
        _editar_entidade(dados, 'agendamentos', 'Agendamento', ['data', 'hora', 'status'])
    elif opcao == '5':
        return
    else:
        print("Opção inválida!")

def _editar_entidade(dados, nome_entidade, nome_exibicao, campos):
    """Função auxiliar para editar uma entidade específica"""
    
    print(f"\n--- EDITAR {nome_exibicao.upper()} ---")
    
    # Listar registros existentes
    if not dados[nome_entidade]:
        print(f"Nenhum {nome_exibicao.lower()} cadastrado.")
        return
    
    _listar_registros(dados, nome_entidade, nome_exibicao)
    
    try:
        id_registro = int(input(f"\nID do {nome_exibicao.lower()} a editar: "))
        
        # Encontrar registro
        registro_encontrado = None
        for registro in dados[nome_entidade]:
            if registro['id'] == id_registro:
                registro_encontrado = registro
                break
        
        if not registro_encontrado:
            print(f"{nome_exibicao} não encontrado!")
            return
        
        print(f"\nEditando {nome_exibicao.lower()}:")
        print("Deixe em branco para manter o valor atual.")
        
        # Editar campos
        for campo in campos:
            valor_atual = registro_encontrado.get(campo, '')
            
            if campo == 'preco' and isinstance(valor_atual, (int, float)):
                valor_atual = f"R$ {valor_atual:.2f}"
            
            novo_valor = input(f"{campo.title()} atual ({valor_atual}): ").strip()
            
            if novo_valor:
                # Converter tipos específicos
                if campo == 'preco':
                    try:
                        # Remove 'R$' e espaços, converte para float
                        novo_valor = novo_valor.replace('R$', '').replace(',', '.').strip()
                        registro_encontrado[campo] = float(novo_valor)
                    except ValueError:
                        print("Preço inválido! Mantendo valor anterior.")
                else:
                    registro_encontrado[campo] = novo_valor
        
        salvar_dados(dados)
        print(f"{nome_exibicao} atualizado com sucesso!")
        
    except ValueError:
        print("ID inválido!")

def _listar_registros(dados, nome_entidade, nome_exibicao):
    """Lista registros de forma genérica"""
    
    print(f"\n{nome_exibicao.upper()}S CADASTRADOS:")
    
    for registro in dados[nome_entidade]:
        if nome_entidade == 'clientes':
            print(f"ID: {registro['id']} | Nome: {registro['nome']} | Telefone: {registro['telefone']} | E-mail: {registro['email']}")
        
        elif nome_entidade == 'carros':
            # Encontrar nome do cliente
            nome_cliente = "Cliente não encontrado"
            for cliente in dados['clientes']:
                if cliente['id'] == registro['id_cliente']:
                    nome_cliente = cliente['nome']
                    break
            print(f"ID: {registro['id']} | Modelo: {registro['modelo']} | Placa: {registro['placa']} | Cor: {registro['cor']} | Cliente: {nome_cliente}")
        
        elif nome_entidade == 'tipos_lavagem':
            print(f"ID: {registro['id']} | Descrição: {registro['descricao']} | Preço: R$ {registro['preco']:.2f} | Tempo: {registro['tempo_medio']}")
        
        elif nome_entidade == 'agendamentos':
            # Encontrar informações relacionadas
            nome_cliente = "Cliente não encontrado"
            for cliente in dados['clientes']:
                if cliente['id'] == registro['id_cliente']:
                    nome_cliente = cliente['nome']
                    break
            
            modelo_carro = "Carro não encontrado"
            for carro in dados['carros']:
                if carro['id'] == registro['id_carro']:
                    modelo_carro = carro['modelo']
                    break
            
            descricao_lavagem = "Lavagem não encontrada"
            for lavagem in dados['tipos_lavagem']:
                if lavagem['id'] == registro['id_lavagem']:
                    descricao_lavagem = lavagem['descricao']
                    break
            
            print(f"ID: {registro['id']} | Cliente: {nome_cliente} | Carro: {modelo_carro}")
            print(f"   Lavagem: {descricao_lavagem} | Data: {registro['data']} {registro['hora']} | Status: {registro['status']}")
            print("-" * 50)