from typing import Text
from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column
from . import Base



class TipoLavagem(Base):
    __tablename__ = 'tb_tipos-labagem'

    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str] = mapped_column(Text, deferred=True)
    preco: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
