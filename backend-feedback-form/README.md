# Back End Feedback Form - FastAPI

## Overview

This project is designed to create a feedback form using FastAPI, SQLAlchemy (with asyncpg), PostgreSQL, Pydantic, and Alembic. It includes both backend and frontend implementations for collecting user feedback with a rating of 1 to 5, where 5 indicates the highest level of satisfaction.

## Installation and Setup

### Python Virtual Environment

To create a Python virtual environment in your project directory:

```bash
python -m venv env

```

Activate the Virtual Environment

```bash
env\Scripts\activate
```

Install Python Dependencies

```bash
pip install fastapi sqlalchemy[asyncio] asyncpg pydantic alembic uvicorn pytest httpx
```

## Database and Alembic Setup

```bash
CREATE DATABASE feedback_db;
```

Update alembic.ini with your database URL:

```bash
sqlalchemy.url = postgresql+asyncpg://<username>:<password>@localhost/feedback_db
```

Alembic Migrations

```bash
alembic init migrations
```

Generate the initial migration script:

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Project Structure

```bash
backend_feedback_form/
├── env/
├── migrations/
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── alembic.ini
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── crud.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── .gitignore
└── README.md
```

# Running the Application

## Start the FastAPI Server

```bash
python -m app.main
```

## API Endpoints

```bash
GET /feedback/ - Retrieve all feedback entries.
POST /feedback/ - Create a new feedback entry.
POST /username/ - Create a new user entry.
```

## Testing

```bash
pytest
```

## Demo

```bash
https://drive.google.com/drive/folders/1TC9TDSI49P0yyAtyK4CLp65czFEXdBJx?usp=drive_link
```
