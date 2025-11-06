import sqlalchemy
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://lavajato_user:rootpassword@localhost:3306/lavajato_db?charset=utf8mb4"  # TODO: ADICIONAR EM VARIAVEL DE AMBIENTE
engine = sqlalchemy.create_engine(
    DATABASE_URL, echo=True
)
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)


def get_session():
    """Dependency-style session generator that always closes the session.

    Useful with frameworks como FastAPI (Depends). Em scripts simples,
    prefira usar `with SessionLocal() as session:` diretamente.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        # Propaga a exceção com uma mensagem mais clara e mantém a traceback original
        raise Exception(f"Erro ao carregar sessão: {e}") from e
    finally:
        db.close()

