from repositories.AgendamentoRepository import AgendamentoRepository
from models.model import Agendamento, Cliente, Carro, TipoLavagem
from faker import Faker
from datetime import datetime, timedelta
import random

def seed_clientes(session, num_records=20):
    fake = Faker()
    clientes = []
    for _ in range(num_records):
        cliente = Cliente(
            nome=fake.name(),
            telefone=fake.phone_number(),
            email=fake.unique.email()
        )
        clientes.append(cliente)
        session.add(cliente)
    session.commit()
    return clientes

def seed_carros(session, clientes, num_records=40):
    fake = Faker()
    carros = []
    for _ in range(num_records):
        cliente = random.choice(clientes)
        carro = Carro(
            id_cliente=cliente.id,
            marca=fake.company(),
            modelo=fake.word().title(),
            ano=random.randint(2000, 2023),
            cor=fake.color_name()
        )
        carros.append(carro)
        session.add(carro)
    session.commit()
    return carros

def seed_tipos_lavagem(session):
    tipos = [
        {"descricao": "Lavagem Simples", "preco": 29.99, "tempo_estimado": 30},
        {"descricao": "Lavagem Completa", "preco": 59.99, "tempo_estimado": 60},
        {"descricao": "Lavagem com Cera", "preco": 79.99, "tempo_estimado": 75},
        {"descricao": "Lavagem Ecológica", "preco": 49.99, "tempo_estimado": 45},
        {"descricao": "Lavagem Premium", "preco": 99.99, "tempo_estimado": 90},
    ]
    for tipo in tipos:
        tipo_lavagem = TipoLavagem(
            descricao=tipo["descricao"],
            preco=tipo["preco"],
            tempo_estimado=tipo["tempo_estimado"]
        )
        session.add(tipo_lavagem)
    session.commit()

def seed_agendamentos(session, num_records=50):
    fake = Faker()
    agendamento_repo = AgendamentoRepository(session)

    for _ in range(num_records):
        data_hora = fake.date_time_between(start_date='now', end_date='+30d')
        cliente_id = random.randint(1, 20)  # Assuming you have 20 clients
        id_carro = random.randint(1, 40)    # Assuming you have 40 cars
        tipo_lavagem_id = random.randint(1, 5)  # Assuming you have 5 types of wash
        status = random.choice(['agendado', 'concluído', 'cancelado'])

        agendamento = Agendamento(
            data_hora=data_hora,
            cliente_id=cliente_id,
            id_carro=id_carro,
            tipo_lavagem_id=tipo_lavagem_id,
            status=status
        )

        agendamento_repo.save(agendamento)

    session.commit()
    
    
    
if __name__ == "__main__":
    from db.session import SessionLocal, engine
    from models.model import Base

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create a new session
    session = SessionLocal()

    # Seed agendamentos
    seed_agendamentos(session, num_records=50)
    seed_carros(session, seed_clientes(session, num_records=20), num_records=40)
    seed_tipos_lavagem(session)

    # Close the session
    session.close()


