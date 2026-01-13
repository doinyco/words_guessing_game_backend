from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import random
import string

from app.db.session import get_db
from app.models import Match
from app.schemas import MatchCreateResponse

router = APIRouter(prefix="/matches", tags=["matches"])

@router.post("/start", response_model=MatchCreateResponse)
def start_match(db: Session = Depends(get_db)):
    """
    Start a new match with a random letter.
    """
    # Generate a random uppercase letter
    letter = random.choice(string.ascii_uppercase)

    # Create a new match
    match = Match(letter=letter)
    db.add(match)
    db.commit()
    db.refresh(match)

    return match