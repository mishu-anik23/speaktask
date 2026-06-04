# Development Setup Guide

## Prerequisites

- Docker & Docker Compose (for easiest setup)
- Python 3.12+ (for local backend dev)
- Node.js 18+ (for local frontend dev)
- Git

## Quick Start (Docker Compose)

```bash
# 1. Clone and navigate
git clone <repo>
cd speaktask

# 2. Create environment file
cp backend/.env.example backend/.env

# 3. Generate secrets
python3 -c "from cryptography.fernet import Fernet; print('FERNET_SECRET=' + Fernet.generate_key().decode())" >> backend/.env
python3 -c "import secrets; print('JWT_SECRET=' + secrets.token_urlsafe(32))" >> backend/.env

# 4. Add your API keys to backend/.env
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# GOOGLE_API_KEY=...
# WHISPER_API_KEY=...

# 5. Start services
docker-compose up

# 6. In new terminal, run migrations
docker-compose exec backend alembic upgrade head

# 7. Visit http://localhost:3000
```

## Local Backend Development

### Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies (optional)
pip install pytest pytest-asyncio

# Setup database
# Option 1: Use Docker PostgreSQL
docker run -d \
  --name postgres \
  -e POSTGRES_DB=speaktask \
  -e POSTGRES_USER=speaktask \
  -e POSTGRES_PASSWORD=speaktask_dev \
  -p 5432:5432 \
  postgres:15-alpine

# Option 2: Use local PostgreSQL
# Create database manually

# Setup Redis
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7-alpine

# Create .env file
cp .env.example .env

# Edit .env with database URL and API keys
nano .env

# Run migrations
alembic upgrade head
```

### Running Services

**Terminal 1 - FastAPI:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Celery Worker:**
```bash
cd backend
source venv/bin/activate
celery -A app.workers.celery worker -l info
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Local Frontend Development

### Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Ensure backend is running on http://localhost:8000
```

### Running

```bash
npm run dev

# Visit http://localhost:3000
```

### Building

```bash
npm run build
npm start
```

## Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## Database Migrations

### Creating Migrations

```bash
cd backend
source venv/bin/activate

# Auto-generate migration based on model changes
alembic revision --autogenerate -m "Add new column"

# Review generated file in alembic/versions/
```

### Applying Migrations

```bash
cd backend
source venv/bin/activate

# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade +1

# Rollback one migration
alembic downgrade -1

# Check current revision
alembic current
```

## Debugging

### Backend

```bash
# Enable debug logging
export DEBUG=True
uvicorn main:app --reload

# Add breakpoints in code:
import pdb; pdb.set_trace()

# Or use Python debugger
import ipdb; ipdb.set_trace()
```

### Frontend

```bash
# Use browser DevTools (F12)
# Console tab for JavaScript errors
# Network tab for API requests
# Application tab for localStorage

# Debug output
console.log("value:", value);
console.table(data);
```

### Docker

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f celery

# Shell into container
docker-compose exec backend bash
docker-compose exec frontend sh

# Restart service
docker-compose restart backend
```

## Common Issues

### Port Already in Use
```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Database Connection Error
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Verify DATABASE_URL in .env
DATABASE_URL=postgresql://user:pass@localhost:5432/speaktask

# Test connection
psql postgresql://speaktask:speaktask_dev@localhost:5432/speaktask
```

### Redis Connection Error
```bash
# Check Redis is running
docker ps | grep redis

# Verify REDIS_URL in .env
REDIS_URL=redis://localhost:6379/0

# Test connection
redis-cli ping  # Should return "PONG"
```

### API Key Issues
- Verify API key format matches provider requirements
- Check key hasn't expired or reached usage limits
- Test directly with provider's API client

### WebSocket Connection Fails
- Verify backend WebSocket endpoint is accessible
- Check NEXT_PUBLIC_WS_URL matches backend URL
- Check browser doesn't have proxy/firewall blocking

### Dependency Installation Issues
If you encounter errors with `pip install -r requirements.txt`:
```bash
# Update pip
pip install --upgrade pip

# Clear pip cache
pip cache purge

# Install with verbose output
pip install -r requirements.txt -v

# Try installing individual packages
pip install fastapi uvicorn sqlalchemy
```

## Code Style

### Python
```bash
# Format code
black app/

# Check style
flake8 app/

# Type checking
mypy app/
```

### TypeScript/JavaScript
```bash
# Format code
prettier --write .

# Lint
eslint .

# Type checking
tsc --noEmit
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://speaktask:speaktask_dev@localhost:5432/speaktask
REDIS_URL=redis://localhost:6379/0
FERNET_SECRET=<generated-key>
JWT_SECRET=<generated-key>
OPENAI_API_KEY=<your-key>
ANTHROPIC_API_KEY=<your-key>
GOOGLE_API_KEY=<your-key>
WHISPER_API_KEY=<your-key>
DEBUG=True
CORS_ORIGINS=["http://localhost:3000"]
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## Useful Commands

```bash
# Reset everything
docker-compose down -v

# View database
docker-compose exec postgres psql -U speaktask -d speaktask

# Monitor Celery
celery -A app.workers.celery inspect active

# View Redis keys
redis-cli keys "*"

# Clear Redis
redis-cli flushall
```

## Documentation

- API: See `docs/api.md`
- Architecture: See `docs/architecture.md`
- Main README: See `README.md`

## Getting Help

1. Check existing issues on GitHub
2. Review logs: `docker-compose logs -f`
3. Test in isolation (test single endpoint, etc.)
4. Create detailed issue with:
   - What you expected
   - What happened
   - Steps to reproduce
   - Relevant logs/screenshots
