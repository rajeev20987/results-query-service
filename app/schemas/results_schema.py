from pydantic import BaseModel


class ResultResponse(BaseModel):
    id: int
    name: str
    status: str
    suite: str

    class Config:
        from_attributes = True  # for ORM compatibility