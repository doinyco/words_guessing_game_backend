from pydantic import BaseModel

# Response schema for creating a new match
class MatchCreateResponse(BaseModel):
    id: int
    letter: str
    status: str

    class Config:
        from_attributes = True

# Request body for joining a match
class MatchJoin(BaseModel):
    player_id: int

# Response schema for joining a match
class MatchJoinResponse(BaseModel):
    match_id: int
    player_id: int
    player_name: str
