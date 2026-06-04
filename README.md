# SpeakTask v1

A voice-command AI web app that routes commands to multiple AI providers (OpenAI, Claude, Gemini) with a modern Next.js frontend and FastAPI backend.

## Features

- 🎤 Voice recording with Web Audio API
- 🤖 Multi-provider AI support (OpenAI, Claude, Gemini)
- 🔐 Encrypted credential storage
- ⚡ Async background job processing with Celery
- 📡 Real-time WebSocket updates
- 📝 Command history and filtering
- 🎨 Modern UI with Tailwind CSS and shadcn/ui

## Tech Stack

**Backend:**
- Python 3.12+, FastAPI, SQLAlchemy 2.x
- PostgreSQL, Redis, Celery
- Alembic for migrations

**Frontend:**
- Next.js 14, React 18, TypeScript
- Tailwind CSS, shadcn/ui
- TanStack React Query

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.12+ (for local backend development)
- PostgreSQL 15+ and Redis 7+ (if not using Docker)

### Using Docker Compose

```bash
# Clone repository
git clone <repo-url>
cd speaktask

# Create .env file with your API keys
cp .env.example .env

# Edit .env with your:
# - OPENAI_API_KEY
# - ANTHROPIC_API_KEY
# - GOOGLE_API_KEY
# - WHISPER_API_KEY
# - FERNET_SECRET (generate: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
# - JWT_SECRET (generate: openssl rand -base64 32)

# Start services
docker-compose up

# Run migrations
docker-compose exec backend alembic upgrade head

# Access app
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Local Development

**Backend setup:**

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Run migrations
alembic upgrade head

# Start FastAPI server
uvicorn main:app --reload

# In another terminal, start Celery worker
celery -A app.workers.celery worker -l info
```

**Frontend setup:**

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local

# Start dev server
npm run dev
```

## Project Structure

```
speaktask/
├── backend/
│   ├── app/
│   │   ├── api/          # API route handlers
│   │   ├── core/         # Config, security, dependencies
│   │   ├── db/           # Database session setup
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── providers/    # AI provider adapters
│   │   └── workers/      # Celery background tasks
│   ├── alembic/          # Database migrations
│   ├── main.py           # FastAPI app entry point
│   └── pyproject.toml
├── frontend/
│   ├── app/              # Next.js App Router
│   ├── components/       # React components
│   ├── hooks/            # Custom React hooks
│   ├── lib/              # API client, types, utilities
│   └── package.json
├── docker-compose.yml
├── .gitignore
└── README.md
```

## API Endpoints

### Auth
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user info

### Commands
- `POST /commands` - Create command
- `GET /commands` - List commands
- `GET /commands/{id}` - Get command details
- `POST /commands/{id}/retry` - Retry failed command

### Voice
- `POST /voice/submit` - Submit audio file
- `POST /voice/transcribe` - Transcribe audio

### Providers
- `GET /providers` - List available providers
- `POST /providers/connect` - Connect provider with API key
- `POST /providers/disconnect` - Disconnect provider
- `GET /providers/status` - Check provider connection status

### Settings
- `GET /settings` - Get user settings
- `PATCH /settings` - Update user settings

### WebSocket
- `WS /ws/commands` - Real-time command status updates

## Environment Variables

### Backend (.env)

```
DATABASE_URL=postgresql://user:pass@localhost:5432/speaktask
REDIS_URL=redis://localhost:6379/0
FERNET_SECRET=<generate-with-Fernet.generate_key()>
JWT_SECRET=<generate-with-openssl>
WHISPER_API_KEY=<your-key>
OPENAI_API_KEY=<your-key>
ANTHROPIC_API_KEY=<your-key>
GOOGLE_API_KEY=<your-key>
DEBUG=False
```

### Frontend (.env.local)

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Development Workflow

1. Make changes in backend/frontend
2. Backend changes auto-reload with `--reload` flag
3. Frontend changes hot-reload automatically
4. Test with `npm test` (frontend) or `pytest` (backend)
5. Check types with `mypy` (Python) or `tsc` (TypeScript)

## Testing

### Backend

```bash
cd backend
pytest tests/
```

### Frontend

```bash
cd frontend
npm test
```

## Deployment

### Railway / Fly.io

1. Create accounts on platform
2. Link git repository
3. Set environment variables in dashboard
4. Platform auto-deploys on push to main

### Self-hosted (VPS)

1. Install Docker and Docker Compose
2. Clone repository
3. Set environment variables
4. Run `docker-compose -f docker-compose.prod.yml up -d`
5. Set up Nginx reverse proxy
6. Configure SSL with Let's Encrypt

## Troubleshooting

### Database connection failed
- Check PostgreSQL is running: `docker-compose ps`
- Verify DATABASE_URL in .env
- Check network connectivity

### WebSocket connection fails
- Ensure NEXT_PUBLIC_WS_URL is correct
- Check CORS settings in FastAPI
- Verify WebSocket is not blocked by firewall

### Provider API errors
- Validate API keys in settings page
- Check provider status endpoint
- Review backend logs: `docker-compose logs backend`

## License

MIT

## Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## Support

For issues and questions:
- Check existing issues
- Create new issue with details
- Contact maintainers
