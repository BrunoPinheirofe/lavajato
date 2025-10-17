from models import Base
from db.session import engine

Base.metadata.create_all(bind=engine)
# Cria todas as tabelas no banco de dados
# (se já existirem, não faz nada)