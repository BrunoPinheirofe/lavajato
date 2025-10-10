# lavagens.py
import json
from database import carregar_dados, salvar_dados

# Preços pré-definidos para cada tipo de lavagem
PRECOS_PREDEFINIDOS = {
    'Lavagem Simples': 25.00,
    'Lavagem Completa': 60.00,
    'Lavagem Premium': 120.00,
    'Polimento': 80.00,
    'Higienização Interna': 45.00,
    'Lavagem a Seco': 35.00,
    'Cristalização': 150.00
}

def cadastrar_tipo_lavagem():
    """Cadastra um novo tipo de lavagem com preço pré-definido"""
    dados = carregar_dados()
    
    print("\n" + "=" * 50)
    print("🧼 CADASTRO DE TIPO DE LAVAGEM")
    print("=" * 50)
    
    # Mostrar opções pré-definidas
    print("\n📋 TIPOS DE LAVAGEM PRÉ-DEFINIDOS:")
    print("-" * 45)
    
    tipos_disponiveis = []
    for i, (descricao, preco) in enumerate(PRECOS_PREDEFINIDOS.items(), 1):
        # Verificar se já não foi cadastrado
        ja_cadastrado = any(l['descricao'] == descricao for l in dados['tipos_lavagem'])
        status = "✅ Já cadastrado" if ja_cadastrado else "📝 Disponível"
        
        print(f"{i:2}. {descricao:25} | R$ {preco:6.2f} | {status}")
        if not ja_cadastrado:
            tipos_disponiveis.append((descricao, preco))
    
    print("\n💡 Escolha uma opção pré-definida ou digite um novo tipo")
    print("   (Para tipos personalizados, o preço será definido automaticamente)")
    
    opcao = input("\n📍 Número da opção ou novo tipo: ").strip()
    
    descricao = ""
    preco = 0.0
    
    # Verificar se escolheu uma opção numérica
    if opcao.isdigit():
        idx = int(opcao) - 1
        if 0 <= idx < len(tipos_disponiveis):
            descricao, preco = tipos_disponiveis[idx]
            print(f"✅ Selecionado: {descricao} - R$ {preco:.2f}")
        else:
            print("❌ Opção inválida!")
            return
    else:
        # Tipo personalizado - definir preço baseado no nome
        descricao = opcao
        preco = _definir_preco_automatico(descricao)
        print(f"💡 Preço definido automaticamente: R$ {preco:.2f}")
    
    tempo_medio = input("⏰ Tempo médio (ex: 30 minutos): ")
    
    # Verificar se já existe
    if any(l['descricao'].lower() == descricao.lower() for l in dados['tipos_lavagem']):
        print(f"❌ '{descricao}' já está cadastrado!")
        return
    
    # Gerar ID automático
    if dados['tipos_lavagem']:
        novo_id = max(lavagem['id'] for lavagem in dados['tipos_lavagem']) + 1
    else:
        novo_id = 1
    
    tipo_lavagem = {
        'id': novo_id,
        'descricao': descricao,
        'preco': preco,
        'tempo_medio': tempo_medio
    }
    
    dados['tipos_lavagem'].append(tipo_lavagem)
    salvar_dados(dados)
    
    print(f"\n✅ Tipo de lavagem cadastrado com sucesso!")
    print(f"   📋 ID: {novo_id}")
    print(f"   🧼 Serviço: {descricao}")
    print(f"   💵 Preço: R$ {preco:.2f} (FIXO)")
    print(f"   ⏰ Tempo: {tempo_medio}")

def _definir_preco_automatico(descricao):
    """Define preço automaticamente baseado nas palavras-chave"""
    descricao_lower = descricao.lower()
    
    if any(palavra in descricao_lower for palavra in ['simples', 'básic', 'rapid']):
        return 25.00
    elif any(palavra in descricao_lower for palavra in ['complet', 'full', 'total']):
        return 60.00
    elif any(palavra in descricao_lower for palavra in ['premium', 'luxo', 'executiv']):
        return 120.00
    elif any(palavra in descricao_lower for palavra in ['polit', 'brilho', 'cristal']):
        return 80.00
    elif any(palavra in descricao_lower for palavra in ['higien', 'intern', 'limpeza']):
        return 45.00
    elif any(palavra in descricao_lower for palavra in ['seco', 'dry']):
        return 35.00
    else:
        # Preço padrão para tipos desconhecidos
        return 40.00

def listar_tipos_lavagem():
    """Lista todos os tipos de lavagem de forma organizada"""
    dados = carregar_dados()
    
    print("\n" + "=" * 65)
    print("🧼 CATÁLOGO DE SERVIÇOS - PREÇOS FIXOS")
    print("=" * 65)
    
    if not dados['tipos_lavagem']:
        print("📭 Nenhum tipo de lavagem cadastrado.")
        print("💡 Use a opção 1 para cadastrar serviços.")
        return
    
    # Ordenar por preço (do menor para o maior)
    tipos_ordenados = sorted(dados['tipos_lavagem'], key=lambda x: x['preco'])
    
    for lavagem in tipos_ordenados:
        print(f"ID: {lavagem['id']} | {lavagem['descricao']:25} | R$ {lavagem['preco']:7.2f} | ⏱️  {lavagem['tempo_medio']}")
    
    print("=" * 65)
    print(f"📊 Total de serviços: {len(dados['tipos_lavagem'])}")

def criar_tipos_predefinidos():
    """Cria tipos de lavagem pré-definidos se não existirem"""
    dados = carregar_dados()
    
    if not dados['tipos_lavagem']:
        print("🔄 Criando tipos de lavagem pré-definidos...")
        
        tipos_predefinidos = [
            {'id': 1, 'descricao': 'Lavagem Simples', 'preco': 25.00, 'tempo_medio': '30 minutos'},
            {'id': 2, 'descricao': 'Lavagem Completa', 'preco': 60.00, 'tempo_medio': '90 minutos'},
            {'id': 3, 'descricao': 'Lavagem Premium', 'preco': 120.00, 'tempo_medio': '120 minutos'}
        ]
        
        dados['tipos_lavagem'] = tipos_predefinidos
        salvar_dados(dados)
        print("✅ Tipos de lavagem pré-definidos criados!")