# AI Server Backend

This is the backend service for the AI Server project, built with FastAPI.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Copy `.env.example` to `.env`
- Update the values in `.env` with your configuration

4. Run the development server:
```bash
uvicorn app.main:app --reload
```

## Project Structure

```
backend/
├── app/
│   ├── api/            # API endpoints
│   ├── core/           # Core functionality
│   ├── db/             # Database models and migrations
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic
│   └── utils/          # Utility functions
├── tests/              # Test files
├── .env               # Environment variables
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Features

- FastAPI framework
- PostgreSQL database with SQLAlchemy ORM
- JWT authentication
- Redis caching
- Celery for async tasks
- Alembic for database migrations
- Pytest for testing

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
