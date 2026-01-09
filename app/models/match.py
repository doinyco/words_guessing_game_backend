from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.db.base import Base

class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active")

    word_submissions: Mapped[list["WordSubmission"]] = relationship(
        back_populates="match",
        cascade="all, delete-orphan"
    )