# SpeakTask Architecture

## System Overview

SpeakTask is a voice-command AI application that allows users to:
1. Record voice commands or type text
2. Route commands to their choice of AI provider (OpenAI, Claude, Gemini)
3. View command history and results
4. Manage provider API keys securely

## Architecture Layers

### Frontend (Next.js)

**Stack:**
- Next.js 14 (App Router)
- React 18 + TypeScript
- Tailwind CSS for styling
- TanStack React Query for server state
- Web Audio API for voice recording

**Key Components:**
- Authentication pages (login, register)
- Dashboard with voice/text input
- History page with filtering
- Settings page for provider management
- Real-time output panel via WebSocket

### Backend (FastAPI)

**Stack:**
- FastAPI for async HTTP API
- SQLAlchemy 2.x for ORM
- Pydantic v2 for validation
- Alembic for migrations
- PostgreSQL for persistent data
- Redis for caching and job queue

**API Modules:**
- `auth.py` - Authentication endpoints
- `commands.py` - Command CRUD operations
- `voice.py` - Audio upload and transcription
- `providers.py` - Provider credential management
- `settings.py` - User settings
- `realtime.py` - WebSocket connections

### Background Jobs (Celery)

**Tasks:**
- `execute_command_task` - Main command execution
  - Fetches command from DB
  - Routes to provider
  - Executes via provider adapter
  - Updates command status
  - Publishes results via WebSocket

**Queue:** Redis-backed with exponential backoff retry

### Database Schema

**Core Tables:**
- `users` - User accounts
- `provider_accounts` - Encrypted API keys (per provider)
- `commands` - Command records (voice or text input)
- `command_runs` - Execution results and status
- `transcripts` - Voice transcription records
- `execution_logs` - Detailed execution logs
- `settings` - User preferences
- `audit_logs` - Security and compliance logging

## Key Design Decisions

### 1. Async Everything
- FastAPI async endpoints for I/O operations
- Async database session with SQLAlchemy 2.x
- Async provider adapters for HTTP calls
- Ensures high concurrency under load

### 2. Background Job Processing
- Celery decouples command execution from HTTP requests
- User gets immediate response with `command_id`
- WebSocket delivers results when ready
- Graceful error handling with retries

### 3. Provider Adapter Pattern
- Base `ProviderAdapter` class defines interface
- Each provider (OpenAI, Claude, Gemini) implements adapter
- Factory pattern creates correct adapter at runtime
- Easy to add new providers

### 4. Encryption at Rest
- User API keys encrypted with Fernet (cryptography library)
- Encryption key loaded from environment (not committed)
- Keys never appear in logs or responses

### 5. WebSocket for Real-time Updates
- Command execution status streamed to frontend
- Clients connect with WebSocket on command submit
- Broadcast pattern sends updates to all listeners
- Fallback to polling if WebSocket unavailable

### 6. Intent Routing (v1 - Simplified)
- Keyword-based routing (e.g., "using Claude" → Claude provider)
- Falls back to user's default provider
- v2 can enhance with LLM-based intent classification

## Data Flow

### Voice Command Flow

```
1. User records audio (Web Audio API)
   ↓
2. Upload to POST /voice/submit
   ↓
3. Save audio file temporarily
   Create Command record (status=queued)
   Emit Celery task: execute_command_task(command_id)
   Return command_id to frontend
   ↓
4. Frontend opens WebSocket: /ws/commands?command_id=42
   ↓
5. Celery worker receives task
   Transcribe audio (Whisper API)
   Route to provider
   ↓
6. Provider adapter executes
   OpenAI/Claude/Gemini API call
   ↓
7. Save result in CommandRun
   Update Command status → succeeded/failed
   Broadcast update via WebSocket
   ↓
8. Frontend receives result
   Display in OutputPanel
   Save to history
```

### Text Command Flow

Same as voice but skip transcription step:
- Raw text becomes prompt directly
- Route to provider
- Execute and return result

## Security Considerations

### Authentication
- JWT tokens stored in HTTP-only cookies (recommended)
- Access tokens with short expiry (24 hours)
- Refresh tokens stored in DB for rotation

### Credential Storage
- API keys never sent over unencrypted connection (HTTPS only)
- Keys encrypted at rest with Fernet
- Keys decrypted only in memory when needed
- Never logged in plaintext

### Rate Limiting
- 30 commands/minute per user (configurable)
- Enforced at FastAPI level with slowapi
- Prevents abuse and API rate limit exhaustion

### Input Validation
- All inputs validated with Pydantic
- Reject unexpected fields
- File size limits (5MB for audio)
- Duration limits (60 seconds for audio)

### Audit Logging
- All sensitive operations logged
- Provider credential changes tracked
- Command execution logged with metadata
- Useful for compliance and debugging

## Scaling Considerations

### Horizontal Scaling

**Frontend:**
- Deploy multiple instances behind load balancer
- Static assets served from CDN
- Session state in browser (localStorage)

**Backend:**
- Multiple FastAPI instances behind reverse proxy
- Shared PostgreSQL database
- Shared Redis for sessions and Celery
- Database connection pooling

**Workers:**
- Multiple Celery workers for task processing
- Auto-scaling based on queue depth
- Priority queues for high-priority tasks

### Caching

**Redis:**
- Cache transcription results
- Rate limit counters
- Session data
- Job queue and results

**Query Optimization:**
- Indexes on foreign keys and timestamps
- Connection pooling
- Query result caching via React Query

## Monitoring & Observability

### Logging
- Structured logging in JSON format
- Log levels: DEBUG, INFO, WARNING, ERROR
- Logs searchable in external service (Datadog, etc.)

### Metrics
- Command count and latency
- Provider API success rates
- Queue depth and worker count
- Database connection pool usage

### Error Tracking
- Sentry integration for exceptions
- Provider API errors logged with full context
- User-facing errors in audit logs

## Development Workflow

1. **Local Development**
   - Docker Compose for PostgreSQL, Redis
   - Hot reload for FastAPI and Next.js
   - Easy provider testing with mock adapters

2. **Testing**
   - Unit tests for provider adapters
   - Integration tests for API endpoints
   - E2E tests for critical flows

3. **Deployment**
   - CI/CD runs tests
   - Build and push Docker images
   - Deploy to target environment

## Future Enhancements

### Phase 2+
- Streaming responses from providers
- Multi-turn conversations with context
- Command templates and shortcuts
- Advanced intent classification (LLM-based)
- Cost tracking and budgets
- Provider failover and load balancing
- Plugin system for custom providers
- Mobile app (React Native)

## Dependencies

**Backend:**
- FastAPI 0.109+
- SQLAlchemy 2.0+
- Pydantic 2.0+
- Celery 5.3+
- Redis 5.0+
- cryptography 41.0+

**Frontend:**
- Next.js 14+
- React 18+
- TypeScript 5+
- Tailwind CSS 3.3+

## Deployment Options

### Cloud Platforms
- **Railway** - Git-based deployment, PostgreSQL included
- **Fly.io** - Global deployment, built-in Redis
- **Heroku** - Traditional PaaS, easy scaling

### Self-Hosted
- VPS (DigitalOcean, Linode, AWS EC2)
- Kubernetes for advanced scaling
- Docker Compose for simple setups

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Celery Documentation](https://docs.celeryproject.io/)
