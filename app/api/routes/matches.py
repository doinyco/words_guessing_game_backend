from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import random
import string

from app.db.session import get_db
from app.models import Match, Player, WordSubmission
from app.schemas import (
    MatchCreateResponse,
    MatchJoinResponse,
    PlayerCreate,
    WordSubmissionCreate,
    WordSubmissionResponse,
)

from app.core.dictionary import is_valid_word

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

@router.post("/{match_id}/join", response_model=MatchJoinResponse)
def join_match(
    match_id: int,
    player: PlayerCreate,
    db: Session = Depends(get_db)
):
    # Check if the match exists
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Create a new player
    new_player = Player(name=player.name)
    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return {
        "match_id": match.id,
        "player_id": new_player.id,
        "player_name": new_player.name
    }


@router.post("/{match_id}/submit", response_model=WordSubmissionResponse)
def submit_word(
    match_id: int,
    player_id: int,
    payload: WordSubmissionCreate,
    db: Session = Depends(get_db),
):
    match = db.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    if match.status != "active":
        raise HTTPException(status_code=400, detail="Match is not active")

    player = db.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    word = payload.word.strip().lower()
    if not word:
        raise HTTPException(status_code=400, detail="Word cannot be empty")

    # validate first letter
    if word[0].upper() != match.letter.upper():
        raise HTTPException(
            status_code=400,
            detail=f"Word must start with '{match.letter.upper()}'",
        )

    # validate word exists
    if not is_valid_word(word):
        raise HTTPException(status_code=400, detail="Word not found in dictionary")

    # prevent duplicates per player per match
    existing = (
        db.query(WordSubmission)
        .filter(
            WordSubmission.match_id == match_id,
            WordSubmission.player_id == player_id,
            WordSubmission.word == word,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Word already submitted")

    submission = WordSubmission(
        match_id=match_id,
        player_id=player_id,
        word=word,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission
   