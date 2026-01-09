from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from app.db.base import Base

class WordSubmission(Base):
    __tablename__ = "word_submissions"

    id: Mapped[int] = mapped_column(primary_key=True)

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False
    )

    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id"),
        nullable=False
    )

    word: Mapped[str] = mapped_column(String(50), nullable=False)

    player: Mapped["Player"] = relationship(back_populates="word_submissions")
    match: Mapped["Match"] = relationship(back_populates="word_submissions")