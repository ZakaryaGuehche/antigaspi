from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Panier(Base):
    __tablename__ = "paniers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    commerce: Mapped[str] = mapped_column(String(100))
    titre: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500), default="")
    prix_initial: Mapped[float] = mapped_column(Float)
    prix_reduit: Mapped[float] = mapped_column(Float)
    quantite: Mapped[int] = mapped_column(Integer, default=1)
    cree_le: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())