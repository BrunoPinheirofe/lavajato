from flask import Blueprint, render_template, request, redirect, url_for
from db.session import SessionLocal
from repositories.AgendamentoRepository import AgendamentoRepository
from repositories.ClienteRepository import ClienteRepository
from repositories.CarroRepository import CarroRepository
from repositories.TipoLavagemRepository import TipoLavagemRepository
from model import Agendamento
import datetime

agendamento_bp = Blueprint('agendamento', __name__, url_prefix='/agendamentos')

@agendamento_bp.route('/')
def index():
    db_session = SessionLocal()
    agendamento_repo = AgendamentoRepository(db_session)
    agendamentos = agendamento_repo.get_all_agendamentos()
    db_session.close()
    return render_template('agendamentos/agendamentos.html', agendamentos=agendamentos)

@agendamento_bp.route('/novo', methods=['GET', 'POST'])
def novo_agendamento():
    if request.method == 'POST':
        data_str = request.form['data']
        hora_str = request.form['hora']
        data_hora = datetime.datetime.strptime(f'{data_str} {hora_str}', '%Y-%m-%d %H:%M')
        
        id_carro = request.form['id_carro']
        tipo_lavagem_id = request.form['tipo_lavagem_id']
        
        agendamento = Agendamento(
            data_hora=data_hora,
            id_carro=id_carro,
            tipo_lavagem_id=tipo_lavagem_id,
            status='Agendado',
            data=datetime.datetime.utcnow()
        )
        
        db_session = SessionLocal()
        agendamento_repo = AgendamentoRepository(db_session)
        agendamento_repo.create_agendamento(agendamento)
        db_session.close()
        return redirect(url_for('agendamento.index'))

    db_session = SessionLocal()
    cliente_repo = ClienteRepository(db_session)
    carro_repo = CarroRepository(db_session)
    tipo_lavagem_repo = TipoLavagemRepository(db_session)
    
    clientes = cliente_repo.get_all_clientes()
    carros = carro_repo.get_all_carros()
    tipos_lavagem = tipo_lavagem_repo.get_all_tipos_lavagem()
    
    db_session.close()
    
    return render_template(
        'agendamentos/novo_agendamento.html',
        clientes=clientes,
        carros=carros,
        tipos_lavagem=tipos_lavagem
    )
