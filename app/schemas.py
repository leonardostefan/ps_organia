from pydantic import BaseModel, validator

class ReviewBase(BaseModel):
    text: str
    
class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(ReviewBase):
    sentiment: str = None
    
class Review(ReviewBase):
    id: int
    costumer_name:str
    text:str
    sentiment:str
    created_at: str
    class Config:
        orm_mode = True