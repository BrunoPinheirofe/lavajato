from repositories.AgendamentoRepository import AgendamentoRepository
from repositories.ClienteRepository import ClienteRepository
from repositories.CarroRepository import CarroRepository
from repositories.TipoLavagemRepository import TipoLavagemRepository
from models.model import Agendamento, Cliente, Carro, TipoLavagem
from faker import Faker
from datetime import datetime, timedelta
import random

def seed_clientes(session, num_records=20):
    fake = Faker('pt_BR')
    clientes = []
    for _ in range(num_records):
        cliente = Cliente(
            nome=fake.name(),
            telefone=fake.phone_number().removeprefix('+55 '),
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

def seed_agendamentos(session, num_records=50, clientes=None, carros=None, tipos_lavagem=None):
    fake = Faker()
    agendamento_repo = AgendamentoRepository(session)
    
    clientes = clientes if clientes is not None else ClienteRepository.get_all_clientes(session)
    carros = carros if carros is not None else CarroRepository.get_all_carros(session)
    tipos_lavagem = tipos_lavagem if tipos_lavagem is not None else TipoLavagemRepository.get_all_tipos_lavagem(session)

    for _ in range(num_records):
        data_hora = fake.date_time_between(start_date='now', end_date='+30d')
        cliente_id = random.choice(clientes).id 
        id_carro = random.choice(carros).id
        tipo_lavagem_id = random.choice(tipos_lavagem).id
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

    # Create repository instances
    cliente_repo = ClienteRepository(session)
    carro_repo = CarroRepository(session)
    tipo_lavagem_repo = TipoLavagemRepository(session)

    # Seed
    # seed_clientes(session, num_records=20)
   
    seed_carros(session, cliente_repo.get_all_clientes(), num_records=40)
    seed_tipos_lavagem(session)
    seed_agendamentos(session, num_records=50, 
                    clientes=cliente_repo.get_all_clientes(),
                    carros=carro_repo.get_all_carros(),
                    tipos_lavagem=tipo_lavagem_repo.get_all_tipos_lavagem())
    # Close the session
    session.close()


