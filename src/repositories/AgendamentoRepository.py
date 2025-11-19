

from model import Agendamento, TipoLavagem, Carro
from datetime import datetime
from sqlalchemy.orm import joinedload, undefer

class AgendamentoRepository:
    def __init__(self, session):
        self.session = session
        
    def get_all_agendamentos(self):
        return self.session.query(Agendamento).options(
            joinedload(Agendamento.carro).joinedload(Carro.cliente),
            joinedload(Agendamento.tipo_lavagem).undefer(TipoLavagem.descricao)
        ).all()
    
    
    def get_proximos_agendamentos(self, limit=5):
        hoje = datetime.now()
        return self.session.query(Agendamento).options(
            joinedload(Agendamento.carro).joinedload(Carro.cliente),
            joinedload(Agendamento.tipo_lavagem).undefer(TipoLavagem.descricao)
        ).filter(
            Agendamento.data_hora >= hoje,
            Agendamento.status.in_(['Agendado', 'Em Andamento'])
        ).order_by(Agendamento.data_hora).limit(limit).all()

    def create_agendamento(self, agendamento):
        self.session.add(agendamento)
        self.session.commit()
        return agendamento