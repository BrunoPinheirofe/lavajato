
from . import Base
from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Agendamento(Base):
    __tablename__ = 'tb_agendamentos'

    id: Mapped[int] = mapped_column(primary_key=True)
    data_hora: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    cliente_id: Mapped[int] = mapped_column(ForeignKey('tb_clientes.id'), nullable=False)
    tipo_lavagem_id: Mapped[int] = mapped_column(ForeignKey('tb_tipos-lavagem.id'), nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    