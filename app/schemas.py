from pydantic import BaseModel
from uuid import UUID


class SessionCreate(BaseModel):
    name: str

class SessionResponse(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: UUID
    session_id: UUID
    role: str
    content: str

    class Config:
        orm_mode = True