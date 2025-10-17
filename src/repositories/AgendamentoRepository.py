

class AgendamentoRepository:
    def __init__(self, session):
        self.session = session
        
    def save(self, agendamento):
        self.session.add(agendamento)
        self.session.commit()
        self.session.refresh(agendamento)
        return agendamento