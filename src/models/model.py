from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass

class Agendamento(Base):
    __tablename__ = 'tb_agendamentos'

    id: Mapped[int] = mapped_column(primary_key=True)
    data_hora: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    cliente_id: Mapped[int] = mapped_column(ForeignKey('tb_clientes.id'), nullable=False)
    id_carro: Mapped[int] = mapped_column(ForeignKey('tb_carros.id'), nullable=False)
    tipo_lavagem_id: Mapped[int] = mapped_column(ForeignKey('tb_tipos-lavagem.id'), nullable=False)
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    status: Mapped[str] = mapped_column(nullable=False) # e.g., 'agendado', 'concluído', 'cancelado'

class Cliente(Base):
    __tablename__ = "tb_clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    telefone: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    carros = relationship("Carro", back_populates="cliente")

class Carro(Base):
    __tablename__ = "tb_carros"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("tb_clientes.id"))
    marca: Mapped[str] = mapped_column(nullable=False)
    modelo: Mapped[str] = mapped_column(nullable=False)
    ano: Mapped[int] = mapped_column(nullable=False)
    cor: Mapped[str] = mapped_column(nullable=False)
    cliente = relationship("Cliente", back_populates="carros")

class TipoLavagem(Base):
    __tablename__ = 'tb_tipos-lavagem'

    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str] = mapped_column(Text, deferred=True)
    preco: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    tempo_estimado: Mapped[int] = mapped_column(nullable=False)  # em minutos
