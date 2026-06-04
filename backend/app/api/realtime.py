from fastapi import APIRouter, WebSocket, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.models import Command
import json

router = APIRouter(tags=["realtime"])

# Store active connections
active_connections: dict = {}


@router.websocket("/ws/commands")
async def websocket_endpoint(
    websocket: WebSocket,
    command_id: int = Query(...),
    token: str = Query(None),
):
    """WebSocket connection for real-time command status updates."""
    await websocket.accept()

    try:
        # TODO: Verify token and extract user_id
        user_id = 1  # Placeholder

        # Store connection
        if command_id not in active_connections:
            active_connections[command_id] = []
        active_connections[command_id].append((websocket, user_id))

        while True:
            data = await websocket.receive_text()
            # Echo back for now, will be replaced with actual updates
            await websocket.send_text(json.dumps({"type": "pong"}))

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if command_id in active_connections:
            active_connections[command_id] = [
                (ws, uid)
                for ws, uid in active_connections[command_id]
                if ws != websocket
            ]


async def broadcast_command_update(command_id: int, update: dict):
    """Broadcast command status update to all connected clients."""
    if command_id in active_connections:
        for websocket, _ in active_connections[command_id]:
            try:
                await websocket.send_text(json.dumps(update))
            except Exception as e:
                print(f"Broadcast error: {e}")
