import os
import sys

# Garante que o diretório raiz do projeto esteja no sys.path para suportar imports "src.*"
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.db.session import SessionLocal, engine
from src.models.Cliente import Cliente

# Contrato simples:
# - Inputs: nome, telefone, email
# - Output: Cliente persistido com id preenchido

def salvar_cliente(nome: str, telefone: str, email: str) -> Cliente:
    # Abre e garante fechamento automático da sessão
    with SessionLocal() as session:
        # Cria a tabela do Cliente se ainda não existir (não mexe nas demais)
        Cliente.__table__.create(bind=engine, checkfirst=True)
        novo = Cliente(nome=nome, telefone=telefone, email=email)
        session.add(novo)
        session.commit()   # efetiva no banco
        session.refresh(novo)  # carrega ID gerado
        return novo


if __name__ == "__main__":
    cliente = salvar_cliente(
        nome="Fulano de Tal",
        telefone="(11) 99999-0000",
        email="fulano@example.com",
    )
    print(f"Cliente salvo: id={cliente.id}, nome={cliente.nome}")
