# SpeakTask v1 API Documentation

## Base URL

- Development: `http://localhost:8000`
- Production: Will be configured during deployment

## Authentication

All endpoints except `/auth/register` and `/auth/login` require Bearer token authentication:

```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication

#### Register User
```
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response (200):
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Login User
```
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response (200):
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Get Current User
```
GET /auth/me
Authorization: Bearer <token>

Response (200):
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2024-01-15T10:30:00"
}
```

### Commands

#### Create Command
```
POST /commands
Authorization: Bearer <token>
Content-Type: application/json

{
  "input_type": "text",
  "raw_input": "What is the capital of France?",
  "selected_provider": "openai"
}

Response (200):
{
  "id": 42,
  "status": "queued"
}
```

#### List Commands
```
GET /commands?limit=50&offset=0&provider=openai&status=succeeded
Authorization: Bearer <token>

Response (200):
[
  {
    "id": 42,
    "input_type": "text",
    "raw_input": "What is the capital of France?",
    "selected_provider": "openai",
    "status": "succeeded",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

#### Get Command Details
```
GET /commands/42
Authorization: Bearer <token>

Response (200):
{
  "id": 42,
  "input_type": "text",
  "raw_input": "What is the capital of France?",
  "transcript_text": null,
  "selected_provider": "openai",
  "status": "succeeded",
  "created_at": "2024-01-15T10:30:00",
  "runs": [
    {
      "id": 1,
      "started_at": "2024-01-15T10:30:05",
      "completed_at": "2024-01-15T10:30:08",
      "result_text": "Paris is the capital of France.",
      "error_message": null,
      "tokens_used": 45,
      "cost_estimate": "$0.001"
    }
  ]
}
```

#### Retry Command
```
POST /commands/42/retry
Authorization: Bearer <token>

Response (200):
{
  "id": 42,
  "status": "queued"
}
```

### Voice

#### Submit Voice Command
```
POST /voice/submit
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <audio.wav>
selected_provider: "openai" (optional)

Response (200):
{
  "command_id": 42,
  "status": "processing"
}
```

#### Transcribe Audio
```
POST /voice/transcribe
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <audio.wav>

Response (200):
{
  "transcript_text": "What is the capital of France?"
}
```

### Providers

#### List Providers
```
GET /providers
Authorization: Bearer <token>

Response (200):
[
  {
    "name": "openai",
    "connected": true
  },
  {
    "name": "claude",
    "connected": false
  },
  {
    "name": "gemini",
    "connected": false
  }
]
```

#### Connect Provider
```
POST /providers/connect
Authorization: Bearer <token>
Content-Type: application/json

{
  "provider_name": "openai",
  "credentials": {
    "api_key": "sk-..."
  }
}

Response (200):
{
  "status": "connected",
  "provider": "openai"
}
```

#### Disconnect Provider
```
POST /providers/disconnect?provider_name=openai
Authorization: Bearer <token>

Response (200):
{
  "status": "disconnected",
  "provider": "openai"
}
```

#### Check Provider Status
```
GET /providers/status
Authorization: Bearer <token>

Response (200):
{
  "openai": true,
  "claude": false,
  "gemini": false
}
```

### Settings

#### Get User Settings
```
GET /settings
Authorization: Bearer <token>

Response (200):
[
  {
    "id": 1,
    "key": "default_provider",
    "value": "openai",
    "updated_at": "2024-01-15T10:30:00"
  }
]
```

#### Update Settings
```
PATCH /settings
Authorization: Bearer <token>
Content-Type: application/json

{
  "key": "default_provider",
  "value": "claude"
}

Response (200):
{
  "id": 1,
  "key": "default_provider",
  "value": "claude",
  "updated_at": "2024-01-15T10:35:00"
}
```

### WebSocket

#### Real-time Command Updates
```
WS /ws/commands?command_id=42&token=<access_token>

Messages received:
{
  "type": "status_update",
  "status": "processing",
  "command_id": 42
}

{
  "type": "result",
  "result": "Paris is the capital of France.",
  "tokens_used": 45,
  "command_id": 42
}

{
  "type": "error",
  "error": "API rate limit exceeded",
  "command_id": 42
}
```

## Error Responses

All errors follow this format:

```
{
  "detail": "Error message describing what went wrong"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad request (invalid input)
- `401` - Unauthorized (missing/invalid token)
- `404` - Not found
- `429` - Too many requests (rate limited)
- `500` - Server error

## Rate Limiting

- Commands: 30 per minute per user
- Audio uploads: 5MB max, 60 seconds max duration

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Too Many Requests |
| 500 | Internal Server Error |
