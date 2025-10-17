from . import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Cliente(Base):
    __tablename__ = "tb_clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    telefone: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    carros = relationship("Carro", back_populates="parent")
