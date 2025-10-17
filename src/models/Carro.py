from sqlalchemy import true
from sqlalchemy.orm import Mapped, mapped_column


class Carro:
    def __init__(self):
        __tablename__ = "tb_carros"
        id: Mapped[int] = mapped_column(primary_key=True)

