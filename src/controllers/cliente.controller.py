

class ClienteController:
    def __init__(self, cliente_repository):
        self.cliente_repository = cliente_repository

    def get_cliente(self, cliente_id):
        # Logic to retrieve a cliente by ID
        return self.cliente_repository.get(cliente_id)

    def create_cliente(self, cliente_data):
        # Logic to create a new cliente
        return self.cliente_repository.create(cliente_data)

    def update_cliente(self, cliente_id, cliente_data):
        # Logic to update an existing cliente
        return self.cliente_repository.update(cliente_id, cliente_data)

    def delete_cliente(self, cliente_id):
        # Logic to delete a cliente by ID
        return self.cliente_repository.delete(cliente_id)