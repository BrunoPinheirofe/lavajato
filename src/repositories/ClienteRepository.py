from sqlite3 import IntegrityError
from model import Cliente


class ClienteRepository:
    def __init__(self, db_session):

        self.db_session = db_session

    def create_cliente(self, cliente_data):
        try:
            new_cliente = Cliente(**cliente_data)
            self.db_session.add(new_cliente)
            self.db_session.commit()
            self.db_session.refresh(new_cliente)
            return new_cliente
        except IntegrityError as e:
            self.db_session.rollback()
            print(f"Email já existe: {e}")
        except Exception as e:
            self.db_session.rollback()
            print(f"Erro ao criar cliente: {e}")
            return None

    def get_cliente(self, cliente_id):
        return self.db_session.query(Cliente).filter(Cliente.id == cliente_id).first()

    def get_all_clientes(self):
        return self.db_session.query(Cliente).all()

    def update_cliente(self, cliente_id, cliente_data):
        cliente = self.get_cliente(cliente_id)
        for key, value in cliente_data.items():
            setattr(cliente, key, value)
        self.db_session.commit()
        return cliente

    def delete_cliente(self, cliente_id):
        cliente = self.get_cliente(cliente_id)
        if cliente:
            self.db_session.delete(cliente)
            self.db_session.commit()
        return cliente
