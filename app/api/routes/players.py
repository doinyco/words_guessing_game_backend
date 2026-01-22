from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.player import Player
from app.schemas.player import PlayerCreate, PlayerResponse

router = APIRouter(prefix="/players", tags=["players"])

@router.post("/", response_model=PlayerResponse)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    player = Player(name=player.name)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player