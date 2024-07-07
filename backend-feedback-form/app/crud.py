from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Feedbacks, Users
from app.schemas import FeedbackCreate, FeedbackResponse, UserCreate
from sqlalchemy.future import select

# Create new feedback in the database
async def create_feedback(db: AsyncSession, feedback: FeedbackCreate):
    db_feedback = Feedbacks(        
        score_id=feedback.score_id,
        user_id=feedback.user_id,
        question=feedback.question)
    db.add(db_feedback)
    await db.commit()
    await db.refresh(db_feedback)
    return db_feedback

# Retrieve all feedbacks from the database
async def get_feedback(db: AsyncSession) -> list[FeedbackResponse]:
    statement = select(Feedbacks)
    result = await db.execute(statement)
    feedbacks = result.scalars().all()
    return feedbacks

# Create new username in the database
async def create_username(db: AsyncSession, username: UserCreate):
    db_username = Users(
        username = username.username
    )
    db.add(db_username)
    await db.commit()
    await db.refresh(db_username)
    return db_username
