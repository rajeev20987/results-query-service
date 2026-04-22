from pydantic import BaseModel
from typing import Optional


class ResultResponse(BaseModel):
    id: int
    name: str
    status: str
    suite: str
    trace: Optional[str] = None

    class Config:
        from_attributes = True  # for ORM compatibility