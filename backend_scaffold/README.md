# FastAPI Backend Scaffold for Commercial Project Management System

This scaffold contains a starter FastAPI backend with the following features:
- Project, RA Bill, GST endpoints (CRUD + basic approval flow)
- Pydantic schemas for request/response validation
- SQLAlchemy models and async database setup (can use local Postgres)
- JWT-based auth skeleton (register/login)
- Audit logging hooks (basic)
- Minimal, ready-to-extend codebase

## How to run (development)
1. Create a Python virtualenv and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Set environment variables (example):
   ```bash
   export DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/yourdb
   export SECRET_KEY='change_me'
   ```

3. Start Uvicorn:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Notes
- This scaffold uses SQLAlchemy models in `app/models.py` and Pydantic schemas in `app/schemas.py`.
- Replace the database URL with your local Postgres credentials.
- The scaffold is intentionally small to be easy to extend to your full VBA logic.
