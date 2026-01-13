from pydantic import BaseModel

class PlayerCreate(BaseModel):
    name: str

class PlayerResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True