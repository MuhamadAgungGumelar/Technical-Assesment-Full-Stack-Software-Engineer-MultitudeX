from pydantic import BaseModel

# Schema for creating new feedback
class FeedbackCreate(BaseModel):
    question: str
    score_id: int
    user_id: int

# Schema for returning feedback response
class FeedbackResponse(BaseModel):
    id: int
    question: str
    score_id: int
    user_id: int

    class Config:
        orm_mode = True

# Schema for creating new user
class UserCreate(BaseModel):
    username: str

# Schema for returning user response
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
