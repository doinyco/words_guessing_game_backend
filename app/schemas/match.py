from pydantic import BaseModel

class MatchCreateResponse(BaseModel):
    id: int
    letter: str
    status: str

    class Config:
        from_attributes = True