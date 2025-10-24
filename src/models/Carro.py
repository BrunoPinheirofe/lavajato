from sqlalchemy import true
from sqlalchemy.orm import Mapped, mapped_column


class Carro:
    def __init__(self):
        __tablename__ = "tb_carros"
        id: Mapped[int] = mapped_column(primary_key=True)
        id_cliente: Mapped[int] = mapped_column(nullable=False)
        marca: Mapped[str] = mapped_column(nullable=False)
        modelo: Mapped[str] = mapped_column(nullable=False)
        ano: Mapped[int] = mapped_column(nullable=False)
        cor: Mapped[str] = mapped_column(nullable=False)
