from pydantic import BaseModel
from typing import List
from app.schemas.word_submission import WordSubmissionResponse

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

# Response schema for match details
class MatchDetailResponse(BaseModel):
    id: int
    letter: str
    status: str
    submissions: List[WordSubmissionResponse]

    class Config:
        from_attributes = True

# Leaderboard entry schema
class LeaderBoardEntry(BaseModel):
    player_id: int
    player_name: str
    score: int

# Response schema for match leaderboard
class MatchLeaderBoardResponse(BaseModel):
    match_id: int
    leaderboard: List[LeaderBoardEntry]

class MatchEndResponse(BaseModel):
    id: int
    letter: str
    status: str

    class Config:
        from_attributes = True
