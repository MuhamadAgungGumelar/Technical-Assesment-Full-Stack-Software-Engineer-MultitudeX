from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import SessionLocal
from app.schemas import FeedbackCreate, FeedbackResponse, UserCreate, UserResponse
from app.crud import create_feedback, get_feedback, create_username
import uvicorn

app = FastAPI()

# CORS middleware configuration to allow requests from specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get an asynchronous database session
async def get_db():
    async with SessionLocal() as session:
        yield session

# Endpoint to read all feedbacks
@app.get("/feedback/", response_model=list[FeedbackResponse])
async def read_feedbacks(db: AsyncSession = Depends(get_db)):
    return await get_feedback(db=db)

# Endpoint to create new feedback
@app.post("/feedback/", response_model=FeedbackResponse)
async def create_feedback_view(feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    return await create_feedback(db=db, feedback=feedback)

# Endpoint to create new username
@app.post("/username/", response_model=UserResponse)
async def create_username_view(username: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_username(db=db, username=username)

# Run the FastAPI application with uvicorn server
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
