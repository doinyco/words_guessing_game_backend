from pydantic import BaseModel

class PlayerTimeResponse(BaseModel):
    match_id: int
    player_id: int
    seconds_left: int