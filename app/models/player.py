from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.db.base import Base

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    word_submissions: Mapped[list["WordSubmission"]] = relationship(
        back_populates="player",
        cascade="all, delete-orphan"
    )