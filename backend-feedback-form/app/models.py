from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import configparser

# Read database URL from configuration file
config = configparser.ConfigParser()
config.read('alembic.ini')

DATABASE_URL = config['alembic']['sqlalchemy.url']

# Create an async engine for SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Define Scores table model
class Scores(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)

# Define Users table model
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)

# Define Feedbacks table model
class Feedbacks(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    score_id = Column(Integer, ForeignKey('scores.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    score = relationship("Scores")
    user = relationship("Users")
