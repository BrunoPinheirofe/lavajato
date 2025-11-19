from flask import Flask, render_template, request, redirect, flash
from database import carregar_dados, salvar_dados
from datetime import datetime

app = Flask(__name__)
# Chave secreta ESSENCIAL para que a função 'flash' funcione
app.secret_key = 'chave_secreta_do_lavajato_2025' 

# Status permitidos para Agendamento
STATUS_AGENDAMENTO = ['Agendado', 'Em Andamento', 'Concluído', 'Cancelado']

# =======================================================
# --- FUNÇÕES DE UTILIDADE (Acesso a Dados Limpos) ---
# =======================================================

def get_clientes_raw():
    """Retorna a lista de clientes (dicts) do JSON."""
    return carregar_dados().get('clientes', [])

def get_carros_raw():
    """Retorna a lista de carros (dicts) do JSON."""
    return carregar_dados().get('carros', [])

def get_lavagens_raw():
    """Retorna a lista de lavagens (dicts) do JSON."""
    return carregar_dados().get('tipos_lavagem', [])

def get_agendamentos_raw():
    """Retorna a lista de agendamentos (dicts) do JSON."""
    return carregar_dados().get('agendamentos', [])

def get_agendamentos_com_detalhes():
    """Retorna a lista de agendamentos com detalhes de cliente, carro e serviço
    anexados, no formato adequado para o Dashboard e listagens.
    
    Adiciona 'data_iso' (YYYY-MM-DD) para comparações internas.
    """
    dados = carregar_dados()
    agendamentos = dados.get('agendamentos', [])
    
    clientes_map = {c['id']: c for c in dados.get('clientes', [])}
    carros_map = {ca['id']: ca for ca in dados.get('carros', [])}
    lavagens_map = {l['id']: l for l in dados.get('tipos_lavagem', [])}
    
    agendamentos_processados = []
    for agendamento in agendamentos:
        cliente = clientes_map.get(agendamento.get('id_cliente', 0), {'nome': 'Cliente Desconhecido'})
        carro = carros_map.get(agendamento.get('id_carro', 0), {'modelo': 'Carro Desconhecido', 'placa': 'N/A'})
        lavagem = lavagens_map.get(agendamento.get('id_lavagem', 0), {'descricao': 'Serviço Desconhecido', 'preco': 0.0})
        
        # Converte a data salva (DD/MM/YYYY) para ISO (YYYY-MM-DD) para consistência
        try:
            data_iso = datetime.strptime(agendamento.get('data'), '%d/%m/%Y').strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            data_iso = "2999-01-01" # Coloca datas inválidas no futuro
            
        agendamentos_processados.append({
            'id': agendamento.get('id'),
            'data': agendamento.get('data'), # Formato de exibição: DD/MM/YYYY
            'data_iso': data_iso, # Formato de comparação: YYYY-MM-DD (NOVO CAMPO)
            'hora': agendamento.get('hora'),
            'status': agendamento.get('status'),
            'cliente_nome': cliente['nome'],
            'carro_info': f"{carro['modelo']} ({carro['placa']})",
            'lavagem_descricao': lavagem['descricao'],
            'lavagem_preco': lavagem['preco']
        })

    # Ordena os agendamentos pela data (ISO) e hora
    agendamentos_processados.sort(key=lambda x: (x.get('data_iso'), x.get('hora', '99:99')))
    
    return agendamentos_processados


def calcular_metricas():
    """Calcula as métricas chave para o Dashboard."""
    
    # 1. Utiliza as novas funções de utilidade
    clientes = get_clientes_raw()
    carros = get_carros_raw()
    agendamentos_processados = get_agendamentos_com_detalhes() # Lista de dicionários
    
    total_clientes = len(clientes)
    total_carros = len(carros)
    
    # 2. Corrigida a data para usar o formato ISO (YYYY-MM-DD) para comparação
    hoje_str_iso = datetime.now().strftime('%Y-%m-%d')
    
    agendamentos_hoje = [
        ag for ag in agendamentos_processados 
        if ag.get('data_iso') == hoje_str_iso and ag.get('status') not in ['Cancelado', 'Concluído']
    ]
    
    total_agendamentos_hoje = len(agendamentos_hoje)
    
    faturamento_mes = 0.0
    mes_atual_iso = datetime.now().strftime('%Y-%m')
    
    for ag in agendamentos_processados:
        # Usa 'data_iso' para checar o mês
        if ag.get('status') == 'Concluído' and ag.get('data_iso', '').startswith(mes_atual_iso):
            faturamento_mes += ag.get('lavagem_preco', 0.0)
            
    return{
        'total_clientes': total_clientes,
        'total_carros': total_carros,
        'total_agendamentos_hoje': total_agendamentos_hoje,
        'faturamento_mes': faturamento_mes
    }

# =======================================================
# --- ROTAS DA APLICAÇÃO ---
# =======================================================

# --- ROTA RAIZ (Dashboard) ---
@app.route('/')
def dashboard():
    metricas = calcular_metricas()
    
    # Pega os 5 agendamentos mais próximos (já estão ordenados na função de detalhes)
    agendamentos_proximos = get_agendamentos_com_detalhes()
    
    # Filtra apenas os agendamentos futuros ou de hoje (Agendado/Em Andamento)
    hoje_str_iso = datetime.now().strftime('%Y-%m-%d')
    
    agendamentos_futuros = [
        ag for ag in agendamentos_proximos 
        if ag.get('status') in ['Agendado', 'Em Andamento'] and ag.get('data_iso') >= hoje_str_iso
    ][:5] # Pega os 5 primeiros
    
    return render_template(
        'index.html', # Alterado para dashboard.html
        metricas=metricas,
        agendamentos_proximos=agendamentos_futuros
    )

# ----------------------------------------
# --- ROTAS DE CLIENTE (C, R, U, D) ---
# ----------------------------------------

@app.route('/clientes')
def listar_clientes_web():
    clientes = get_clientes_raw() # Usa a função de utilidade
    return render_template('clientes.html', clientes=clientes)

@app.route('/clientes/novo', methods=['GET', 'POST'])
def cadastrar_cliente_web():
    # ... Lógica original ...
    if request.method == 'GET':
        return render_template('novo_cliente.html')
    
    if request.method == 'POST':
        dados = carregar_dados()
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        
        novo_id = max((c['id'] for c in dados.get('clientes', [])), default=0) + 1
        
        cliente = {'id': novo_id, 'nome': nome, 'telefone': telefone, 'email': email}
        
        if 'clientes' not in dados:
            dados['clientes'] = []
            
        dados['clientes'].append(cliente)
        salvar_dados(dados)
        
        flash(f'Cliente "{nome}" cadastrado com sucesso! ID: {novo_id}', 'success')
        return redirect('/clientes')

@app.route('/clientes/<int:cliente_id>/editar', methods=['GET', 'POST'])
def editar_cliente_web(cliente_id):
    dados = carregar_dados()
    cliente = next((c for c in dados.get('clientes', []) if c['id'] == cliente_id), None)
    
    if not cliente:
        flash(f"❌ Cliente ID {cliente_id} não encontrado.", 'danger')
        return redirect('/clientes')

    if request.method == 'GET':
        return render_template('editar_cliente.html', cliente=cliente)
    
    if request.method == 'POST':
        cliente['nome'] = request.form.get('nome')
        cliente['telefone'] = request.form.get('telefone')
        cliente['email'] = request.form.get('email')
        salvar_dados(dados)
        
        flash(f'✅ Cliente "{cliente["nome"]}" (ID: {cliente_id}) atualizado com sucesso!', 'success')
        return redirect('/clientes')

@app.route('/clientes/<int:cliente_id>/excluir', methods=['POST'])
def excluir_cliente_web(cliente_id):
    dados = carregar_dados()
    
    # 1. Verificar se o cliente tem carros ou agendamentos
    tem_carros = any(c['id_cliente'] == cliente_id for c in dados.get('carros', []))
    tem_agendamentos = any(ag['id_cliente'] == cliente_id for ag in dados.get('agendamentos', []))
    
    if tem_carros or tem_agendamentos:
        flash(f"❌ Não foi possível excluir o Cliente ID {cliente_id}. Ele possui carros e/ou agendamentos associados.", 'danger')
        return redirect('/clientes')

    # 2. Excluir o cliente
    clientes_antes = len(dados.get('clientes', []))
    dados['clientes'] = [c for c in dados.get('clientes', []) if c['id'] != cliente_id]
    clientes_depois = len(dados['clientes'])
    
    if clientes_depois < clientes_antes:
        salvar_dados(dados)
        flash(f"🗑️ Cliente ID {cliente_id} excluído com sucesso!", 'success')
    else:
        flash(f"❌ Cliente ID {cliente_id} não encontrado para exclusão.", 'danger')
        
    return redirect('/clientes')


# ----------------------------------------
# --- ROTAS DE CARRO (C, R, U, D) ---
# ----------------------------------------

@app.route('/carros')
def listar_carros_web():
    dados = carregar_dados()
    carros = dados.get('carros', [])
    clientes_map = {c['id']: c['nome'] for c in dados.get('clientes', [])}
    
    for carro in carros:
        carro['nome_cliente'] = clientes_map.get(carro['id_cliente'], 'Desconhecido')
        
    return render_template('carros.html', carros=carros)

@app.route('/carros/novo', methods=['GET', 'POST'])
def cadastrar_carro_web():
    dados = carregar_dados()
    clientes = dados.get('clientes', [])
    
    if request.method == 'GET':
        return render_template('novo_carro.html', clientes=clientes)
    
    if request.method == 'POST':
        id_cliente = int(request.form.get('id_cliente'))
        modelo = request.form.get('modelo')
        marca = request.form.get('marca')
        placa = request.form.get('placa')
        cor = request.form.get('cor')
        
        novo_id = max((c['id'] for c in dados.get('carros', [])), default=0) + 1
        
        carro = {'id': novo_id, 'id_cliente': id_cliente, 'modelo': modelo, 'marca': marca, 'placa': placa, 'cor': cor}
        
        if 'carros' not in dados:
            dados['carros'] = []
            
        dados['carros'].append(carro)
        salvar_dados(dados)
        
        flash(f'Carro "{modelo}" ({placa}) cadastrado com sucesso! ID: {novo_id}', 'success')
        return redirect('/carros')

@app.route('/carros/<int:carro_id>/editar', methods=['GET', 'POST'])
def editar_carro_web(carro_id):
    dados = carregar_dados()
    carro = next((c for c in dados.get('carros', []) if c['id'] == carro_id), None)
    
    if not carro:
        flash(f"❌ Carro ID {carro_id} não encontrado.", 'danger')
        return redirect('/carros')

    clientes = dados.get('clientes', [])
    
    if request.method == 'GET':
        return render_template('editar_carro.html', carro=carro, clientes=clientes)
    
    if request.method == 'POST':
        carro['id_cliente'] = int(request.form.get('id_cliente'))
        carro['modelo'] = request.form.get('modelo')
        carro['marca'] = request.form.get('marca')
        carro['placa'] = request.form.get('placa')
        carro['cor'] = request.form.get('cor')
        salvar_dados(dados)
        
        flash(f'✅ Carro "{carro["modelo"]}" (ID: {carro_id}) atualizado com sucesso!', 'success')
        return redirect('/carros')

@app.route('/carros/<int:carro_id>/excluir', methods=['POST'])
def excluir_carro_web(carro_id):
    dados = carregar_dados()
    
    # 1. Verificar se o carro tem agendamentos
    tem_agendamentos = any(ag['id_carro'] == carro_id for ag in dados.get('agendamentos', []))
    
    if tem_agendamentos:
        flash(f"❌ Não foi possível excluir o Carro ID {carro_id}. Ele possui agendamentos associados.", 'danger')
        return redirect('/carros')
    
    # 2. Excluir o carro
    carros_antes = len(dados.get('carros', []))
    dados['carros'] = [c for c in dados.get('carros', []) if c['id'] != carro_id]
    carros_depois = len(dados['carros'])
    
    if carros_depois < carros_antes:
        salvar_dados(dados)
        flash(f"🗑️ Carro ID {carro_id} excluído com sucesso!", 'success')
    else:
        flash(f"❌ Carro ID {carro_id} não encontrado para exclusão.", 'danger')
        
    return redirect('/carros')


# ----------------------------------------
# --- ROTAS DE SERVIÇO/LAVAGEM (C, R, U, D) ---
# ----------------------------------------

@app.route('/servicos')
def listar_servicos_web():
    dados = carregar_dados()
    tipos_lavagem = dados.get('tipos_lavagem', [])
    tipos_ordenados = sorted(tipos_lavagem, key=lambda x: x['preco'])
    return render_template('servicos.html', servicos=tipos_ordenados)

@app.route('/servicos/novo', methods=['GET', 'POST'])
def cadastrar_servico_web():
    # --- Requisição GET (Sem Alteração) ---
    if request.method == 'GET':
        # Passa valores vazios para o template em GET
        return render_template('novo_servico.html', descricao="", tempo_medio="", preco_str="")
    
    # --- Requisição POST (Lógica de Validação Corrigida) ---
    if request.method == 'POST':
        dados = carregar_dados()
        # Captura os dados submetidos (manteremos o que foi digitado)
        descricao = request.form.get('descricao')
        tempo_medio = request.form.get('tempo_medio')
        preco_str = request.form.get('preco')
        
        # ⚠️ NOVO BLOCO DE VALIDAÇÃO DE CAMPOS VAZIOS (Recomendado)
        if not descricao or not tempo_medio or not preco_str:
            flash("❌ Todos os campos (Descrição, Tempo e Preço) são obrigatórios.", 'danger')
            # CORREÇÃO: Renderiza o template de novo com os dados submetidos
            return render_template('novo_servico.html', 
                                   descricao=descricao, 
                                   tempo_medio=tempo_medio, 
                                   preco_str=preco_str)

        try:
            # Tenta converter o preço, corrigindo vírgula para ponto
            preco = float(preco_str.replace(',', '.'))
        except ValueError:
            flash("❌ Preço deve ser um número válido (ex: 45.90).", 'danger')
            # 🛑 CORREÇÃO PRINCIPAL: Renderiza o template de novo
            return render_template('novo_servico.html', 
                                   descricao=descricao, 
                                   tempo_medio=tempo_medio, 
                                   preco_str=preco_str) 
        
        # Lógica de cadastro (SE DEU TUDO CERTO)
        novo_id = max((l['id'] for l in dados.get('tipos_lavagem', [])), default=0) + 1
        
        novo_servico = {
            'id': novo_id, 
            'descricao': descricao, 
            'tempo_medio': tempo_medio, 
            'preco': preco
        }
        
        if 'tipos_lavagem' not in dados:
            dados['tipos_lavagem'] = []
            
        dados['tipos_lavagem'].append(novo_servico)
        salvar_dados(dados)
        
        # SUCESSO: Redireciona
        flash(f'Serviço "{descricao}" cadastrado com sucesso! ID: {novo_id}', 'success')
        return redirect('/servicos') # Redirecionamento é bom APENAS para sucesso

@app.route('/servicos/<int:lavagem_id>/editar', methods=['GET', 'POST'])
def editar_lavagem_web(lavagem_id):
    dados = carregar_dados()
    lavagem = next((l for l in dados.get('tipos_lavagem', []) if l['id'] == lavagem_id), None)
    
    if not lavagem:
        flash(f"❌ Serviço ID {lavagem_id} não encontrado.", 'danger')
        return redirect('/servicos')

    if request.method == 'GET':
        return render_template('editar_lavagem.html', lavagem=lavagem)
    
    if request.method == 'POST':
        lavagem['descricao'] = request.form.get('descricao')
        lavagem['tempo_medio'] = request.form.get('tempo_medio')
        
        try:
            preco_str = request.form.get('preco')
            lavagem['preco'] = float(preco_str.replace(',', '.'))
        except ValueError:
            flash("❌ Preço deve ser um número válido (ex: 45.90).", 'danger')
            return redirect(f'/servicos/{lavagem_id}/editar')
        
        salvar_dados(dados)
        
        flash(f'✅ Serviço "{lavagem["descricao"]}" (ID: {lavagem_id}) atualizado com sucesso!', 'success')
        return redirect('/servicos')

@app.route('/servicos/<int:lavagem_id>/excluir', methods=['POST'])
def excluir_lavagem_web(lavagem_id):
    dados = carregar_dados()
    
    # 1. Verificar se o serviço tem agendamentos
    tem_agendamentos = any(ag['id_lavagem'] == lavagem_id for ag in dados.get('agendamentos', []))

    if tem_agendamentos:
        flash(f"❌ Não foi possível excluir o Serviço ID {lavagem_id}. Ele possui agendamentos associados.", 'danger')
        return redirect('/servicos')

    # 2. Excluir o serviço
    lavagens_antes = len(dados.get('tipos_lavagem', []))
    dados['tipos_lavagem'] = [l for l in dados.get('tipos_lavagem', []) if l['id'] != lavagem_id]
    lavagens_depois = len(dados['tipos_lavagem'])
    
    if lavagens_depois < lavagens_antes:
        salvar_dados(dados)
        flash(f"🗑️ Serviço ID {lavagem_id} excluído com sucesso!", 'success')
    else:
        flash(f"❌ Serviço ID {lavagem_id} não encontrado.", 'danger')
        
    return redirect('/servicos')


# ---------------------------------------------
# --- ROTAS DE AGENDAMENTO (C, R, U, D, Detalhes) ---
# ---------------------------------------------

@app.route('/agendamentos')
def listar_agendamentos_web():
    # Usa a função de utilidade para obter a lista processada e ordenada
    agendamentos_processados = get_agendamentos_com_detalhes() 
    
    return render_template('agendamentos.html', agendamentos=agendamentos_processados)

@app.route('/agendamentos/novo', methods=['GET', 'POST'])
def cadastrar_agendamento_web():
    dados = carregar_dados()
    clientes = dados.get('clientes', [])
    carros = dados.get('carros', [])
    tipos_lavagem = dados.get('tipos_lavagem', [])
    
    if request.method == 'GET':
        if not clientes or not carros or not tipos_lavagem:
            flash("❌ Faltam dados essenciais (Cliente, Carro ou Serviço) para agendar.", 'danger')
            return redirect('/')
            
        return render_template('novo_agendamento.html', 
                               clientes=clientes, 
                               carros=carros, 
                               lavagens=tipos_lavagem)
    
    if request.method == 'POST':
        id_cliente = int(request.form.get('id_cliente'))
        id_carro = int(request.form.get('id_carro'))
        id_lavagem = int(request.form.get('id_lavagem'))
        data = request.form.get('data') 
        hora = request.form.get('hora')
        
        try:
            # Converte a data de YYYY-MM-DD (input HTML) para DD/MM/YYYY (storage)
            data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')
        except ValueError:
            flash("❌ Data inválida.", 'danger')
            return redirect('/agendamentos/novo')
        
        novo_id = max((ag['id'] for ag in dados.get('agendamentos', [])), default=0) + 1
            
        novo_agendamento = {
            'id': novo_id,
            'id_cliente': id_cliente,
            'id_carro': id_carro,
            'id_lavagem': id_lavagem,
            'data': data_formatada,
            'hora': hora,
            'status': 'Agendado' 
        }
        
        if 'agendamentos' not in dados:
            dados['agendamentos'] = []
            
        dados['agendamentos'].append(novo_agendamento)
        salvar_dados(dados)
        
        flash(f'🎉 Agendamento #{novo_id} criado com sucesso!', 'success')
        return redirect('/agendamentos')

@app.route('/agendamentos/<int:agendamento_id>')
def detalhes_agendamento_web(agendamento_id):
    dados = carregar_dados()
    agendamento_info = get_agendamentos_com_detalhes()
    agendamento_detalhe = next((ag for ag in agendamento_info if ag['id'] == agendamento_id), None)
    
    if not agendamento_detalhe:
        flash(f"❌ Agendamento ID {agendamento_id} não encontrado.", 'danger')
        return redirect('/agendamentos') 
    
    # Busca os dados brutos para a página de detalhes
    clientes_map = {c['id']: c for c in dados.get('clientes', [])}
    carros_map = {ca['id']: ca for ca in dados.get('carros', [])}
    lavagens_map = {l['id']: l for l in dados.get('tipos_lavagem', [])}
    
    cliente = clientes_map.get(agendamento_detalhe['id_cliente'], {'nome': 'Desconhecido', 'id': agendamento_detalhe['id_cliente'], 'telefone': 'N/A', 'email': 'N/A'})
    carro = carros_map.get(agendamento_detalhe['id_carro'], {'modelo': 'Desconhecido', 'placa': 'N/A', 'id': agendamento_detalhe['id_carro'], 'marca': 'N/A', 'cor': 'N/A'})
    lavagem = lavagens_map.get(agendamento_detalhe['id_lavagem'], {'descricao': 'Desconhecido', 'preco': 0.0, 'id': agendamento_detalhe['id_lavagem'], 'tempo_medio': 'N/A'})
    
    contexto = {
        'agendamento': agendamento_detalhe,
        'cliente': cliente,
        'carro': carro,
        'lavagem': lavagem
    }
    
    return render_template('detalhes_agendamento.html', **contexto)

@app.route('/agendamentos/<int:agendamento_id>/editar', methods=['GET', 'POST'])
def editar_agendamento_web(agendamento_id):
    dados = carregar_dados()
    agendamento = next((ag for ag in dados.get('agendamentos', []) if ag['id'] == agendamento_id), None)
    
    if not agendamento:
        flash(f"❌ Agendamento ID {agendamento_id} não encontrado.", 'danger')
        return redirect('/agendamentos') 
        
    clientes_map = {c['id']: c['nome'] for c in dados.get('clientes', [])}
    carros_map = {ca['id']: f"{ca['modelo']} ({ca['placa']})" for ca in dados.get('carros', [])}
    lavagens_map = {l['id']: l['descricao'] for l in dados.get('tipos_lavagem', [])}
    
    contexto = {
        'agendamento': agendamento,
        'cliente_nome': clientes_map.get(agendamento['id_cliente'], 'Cliente não encontrado'),
        'carro_info': carros_map.get(agendamento['id_carro'], 'Carro não encontrado'),
        'lavagem_descricao': lavagens_map.get(agendamento['id_lavagem'], 'Serviço não encontrado'),
        'status_opcoes': STATUS_AGENDAMENTO
    }
        
    if request.method == 'GET':
        return render_template('editar_agendamento.html', **contexto)
    
    if request.method == 'POST':
        novo_status = request.form.get('status')
        
        if novo_status not in STATUS_AGENDAMENTO:
            flash("❌ Status inválido fornecido.", 'danger')
            return redirect(f'/agendamentos/{agendamento_id}/editar')
        
        agendamento['status'] = novo_status
        salvar_dados(dados)
        
        flash(f'✅ Status do Agendamento #{agendamento_id} atualizado para "{novo_status}"!', 'success')
        return redirect('/agendamentos')

@app.route('/agendamentos/<int:agendamento_id>/excluir', methods=['POST'])
def excluir_agendamento_web(agendamento_id):
    dados = carregar_dados()
    
    agendamentos_antes = len(dados.get('agendamentos', []))
    
    # 1. Excluir o agendamento
    dados['agendamentos'] = [ag for ag in dados.get('agendamentos', []) if ag['id'] != agendamento_id]
    agendamentos_depois = len(dados['agendamentos'])
    
    if agendamentos_depois < agendamentos_antes:
        salvar_dados(dados)
        flash(f"🗑️ Agendamento ID {agendamento_id} excluído com sucesso!", 'success')
    else:
        flash(f"❌ Agendamento ID {agendamento_id} não encontrado para exclusão.", 'danger')
        
    return redirect('/agendamentos')

# --- Execução do Servidor ---
if __name__ == '__main__':
    app.run(debug=True)
