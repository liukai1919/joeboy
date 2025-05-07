# AI Server Project

A full-stack AI server application with React frontend and FastAPI backend.

## Project Structure

```
.
├── frontend/          # React frontend application
└── backend/          # FastAPI backend application
```

## Getting Started

### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at http://localhost:3000

### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the development server:
```bash
uvicorn app.main:app --reload
```

The backend API will be available at http://localhost:8000

## Features

### Frontend
- React with TypeScript
- Ant Design Pro components
- Redux Toolkit for state management
- React Query for data fetching
- TailwindCSS for styling

### Backend
- FastAPI framework
- PostgreSQL database
- SQLAlchemy ORM
- JWT authentication
- Redis caching
- Celery for async tasks

## Development

- Frontend development server runs on port 3000
- Backend API server runs on port 8000
- API documentation available at http://localhost:8000/docs
