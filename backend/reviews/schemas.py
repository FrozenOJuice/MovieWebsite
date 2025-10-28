"""Review models, including voting and update payloads."""
from pydantic import BaseModel, Field
from typing import Optional


class Vote(BaseModel):
    vote: bool  # True if helpful


class Usefulness(BaseModel):
    helpful: int = 0
    total_votes: int = 0


class ReviewBase(BaseModel):
    title: str
    rating: int = Field(..., ge=1, le=10)
    text: str


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    title: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=10)
    text: Optional[str] = None


class Review(BaseModel):
    review_id: str
    movie_id: str
    user_id: str
    title: str
    rating: int
    date: str
    text: str
    usefulness: Usefulness = Usefulness()
