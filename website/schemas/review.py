from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Request body for creating a review
class ReviewCreate(BaseModel):
    rating: int
    comment: Optional[str]

# Response model for returning a review
class ReviewOut(ReviewCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True