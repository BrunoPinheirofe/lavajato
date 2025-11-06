from models.model import TipoLavagem


class TipoLavagemRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_tipo_lavagem(self, tipo_lavagem_data):
        try:
            new_tipo_lavagem = TipoLavagem(**tipo_lavagem_data)
            self.db_session.add(new_tipo_lavagem)
            self.db_session.commit()
            self.db_session.refresh(new_tipo_lavagem)
            return new_tipo_lavagem
        except Exception as e:
            self.db_session.rollback()
            print(f"Erro ao criar tipo de lavagem: {e}")
            return None

    def get_tipo_lavagem(self, tipo_lavagem_id):
        return self.db_session.query(TipoLavagem).filter(TipoLavagem.id == tipo_lavagem_id).first()

    def get_all_tipos_lavagem(self):
        return self.db_session.query(TipoLavagem).all()

    def update_tipo_lavagem(self, tipo_lavagem_id, tipo_lavagem_data):
        tipo_lavagem = self.get_tipo_lavagem(tipo_lavagem_id)
        if tipo_lavagem:
            for key, value in tipo_lavagem_data.items():
                setattr(tipo_lavagem, key, value)
            self.db_session.commit()
        return tipo_lavagem

    def delete_tipo_lavagem(self, tipo_lavagem_id):
        tipo_lavagem = self.get_tipo_lavagem(tipo_lavagem_id)
        if tipo_lavagem:
            self.db_session.delete(tipo_lavagem)
            self.db_session.commit()
        return tipo_lavagem
