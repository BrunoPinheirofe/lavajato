from models.model import Carro


class CarroRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def create_carro(self, carro_data):
        try:
            new_carro = Carro(**carro_data)
            self.db_session.add(new_carro)
            self.db_session.commit()
            self.db_session.refresh(new_carro)
            return new_carro
        except Exception as e:
            self.db_session.rollback()
            print(f"Erro ao criar carro: {e}")
            return None

    def get_carro(self, carro_id):
        return self.db_session.query(Carro).filter(Carro.id == carro_id).first()

    def get_carros_by_cliente(self, cliente_id):
        return self.db_session.query(Carro).filter(Carro.id_cliente == cliente_id).all()

    def update_carro(self, carro_id, carro_data):
        carro = self.get_carro(carro_id)
        if carro:
            for key, value in carro_data.items():
                setattr(carro, key, value)
            self.db_session.commit()
        return carro

    def delete_carro(self, carro_id):
        carro = self.get_carro(carro_id)
        if carro:
            self.db_session.delete(carro)
            self.db_session.commit()
        return carro
