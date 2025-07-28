from pydantic import BaseModel


class ReviewBase(BaseModel):
    costumer_name: str
    text: str


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    sentiment: str
    created_at: str

    class Config:
        orm_mode = True
