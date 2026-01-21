# FIN-tasks Development Setup

## Quick Start

To start the full development environment with one command:

```bash
pip install -e .
./dev.py
```

This will:
1. Check if all dependencies are installed
2. Install frontend dependencies if needed
3. Start both backend (FastAPI) and frontend (React/Vite) servers
4. Provide access to the application

## What You'll Get

- **Frontend**: http://localhost:5173 (React + TypeScript + Vite)
- **Backend API**: http://127.0.0.1:7000/api/v1/ (FastAPI)
- **API Documentation**: http://127.0.0.1:7000/docs (Swagger UI)

## Alternative Commands

### Start Everything
```bash
./dev.py
# or
python3 dev.py
# or after installing: fin-tasks-dev
```

### Start Only Backend
```bash
./dev.py --backend-only
```

### Start Only Frontend
```bash
./dev.py --frontend-only
```

## Manual Setup (Alternative)

If you prefer to start servers manually:

### Backend Setup
```bash
pip install -e .
fin-tasks
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Development Workflow

1. **Start development servers**: `./dev.py`
2. **Make changes** to backend code in `src/fin_tasks/` or frontend code in `frontend/src/`
3. **Servers auto-reload** on code changes
4. **Press Ctrl+C** to stop all servers gracefully

## Database Setup

The application uses SQLite by default. Database migrations are handled automatically:

- Database file: `fin-tasks.db` (created automatically)
- Migrations: `alembic/versions/`

## Testing

Run tests with:
```bash
pytest
```

## Code Quality

Format and lint code:
```bash
black .
isort .
flake8 .
mypy .
```

## Troubleshooting

### Backend Won't Start
- Ensure Python dependencies are installed: `pip install -e .`
- Check if port 7000 is available
- Verify PYTHONPATH includes `src/` directory

### Frontend Won't Start
- Ensure Node.js and npm are installed
- Run `npm install` in the `frontend/` directory
- Check if port 5173 is available

### Permission Issues
- Make sure `dev.py` is executable: `chmod +x dev.py`

## Architecture Overview

- **Backend**: FastAPI + SQLAlchemy + Pydantic
- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **State Management**: React Query (TanStack Query)
- **Database**: SQLite with Alembic migrations
- **Styling**: Tailwind CSS with custom design system
