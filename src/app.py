from flask import Flask, jsonify, render_template
from db.session import engine, SessionLocal
from model import Base, Agendamento, TipoLavagem
from repositories.ClienteRepository import ClienteRepository
from repositories.CarroRepository import CarroRepository
from repositories.AgendamentoRepository import AgendamentoRepository
from datetime import datetime, time
from sqlalchemy import func
from controllers.cliente_controller import cliente_bp
from controllers.carro_controller import carro_bp
from controllers.agendamento_controller import agendamento_bp
from controllers.servico_controller import servico_bp

from json import JSONEncoder

app = Flask(__name__)

# Registra os blueprints
app.register_blueprint(cliente_bp)
app.register_blueprint(carro_bp)
app.register_blueprint(agendamento_bp)
app.register_blueprint(servico_bp)

# Cria as tabelas no banco de dados, se não existirem
Base.metadata.create_all(bind=engine)

def calcular_metricas():
    """Calcula as métricas chave para o Dashboard usando o banco de dados."""
    db_session = SessionLocal()
    try:
        cliente_repo = ClienteRepository(db_session)
        carro_repo = CarroRepository(db_session)
        
        total_clientes = len(cliente_repo.get_all_clientes())
        total_carros = len(carro_repo.get_all_carros())
        
        # Agendamentos para hoje (não cancelados ou concluídos)
        hoje_inicio = datetime.combine(datetime.today(), time.min)
        hoje_fim = datetime.combine(datetime.today(), time.max)
        
        total_agendamentos_hoje = db_session.query(Agendamento).filter(
            Agendamento.data_hora >= hoje_inicio,
            Agendamento.data_hora <= hoje_fim,
            Agendamento.status.notin_(['Cancelado', 'Concluído'])
        ).count()
        
        # Faturamento do mês (agendamentos concluídos)
        mes_atual = datetime.now().month
        ano_atual = datetime.now().year
        
        faturamento_mes = db_session.query(func.sum(TipoLavagem.preco)).join(
            Agendamento, Agendamento.tipo_lavagem_id == TipoLavagem.id
        ).filter(
            func.extract('month', Agendamento.data_hora) == mes_atual,
            func.extract('year', Agendamento.data_hora) == ano_atual,
            Agendamento.status == 'Concluído'
        ).scalar() or 0.0
        
        return {
            'total_clientes': total_clientes,
            'total_carros': total_carros,
            'total_agendamentos_hoje': total_agendamentos_hoje,
            'faturamento_mes': faturamento_mes
        }
    finally:
        db_session.close()

@app.route('/')
def dashboard():
    metricas = calcular_metricas()
    
    agendamentos_proximos = []
    db_session = SessionLocal()
    try:
        agendamento_repo = AgendamentoRepository(db_session)
        # Pega os 5 agendamentos futuros ou de hoje (Agendado/Em Andamento)
        agendamentos_proximos = agendamento_repo.get_proximos_agendamentos(limit=5)
    finally:
        db_session.close()

    return render_template(
        'index.html',
        metricas=metricas,
        agendamentos_proximos=agendamentos_proximos
    )
    

if __name__ == '__main__':
    app.run(debug=True)
