from pydantic import BaseModel

class WordSubmissionCreate(BaseModel):
    word: str

class WordSubmissionResponse(BaseModel):
    id: int
    word: str
    player_id: int
    match_id: int

    class Config:
        from_attributes = True