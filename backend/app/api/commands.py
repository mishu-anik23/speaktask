from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.models import Command, CommandRun
from app.schemas.schemas import CommandCreate, CommandResponse, CommandListResponse
from datetime import datetime
from typing import List

router = APIRouter(prefix="/commands", tags=["commands"])


@router.post("", response_model=dict)
async def create_command(
    command_data: CommandCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new command."""
    command = Command(
        user_id=current_user["user_id"],
        input_type=command_data.input_type,
        raw_input=command_data.raw_input,
        transcript_text=command_data.transcript_text,
        selected_provider=command_data.selected_provider or "openai",
        status="queued",
    )
    db.add(command)
    await db.commit()
    await db.refresh(command)

    # TODO: Trigger Celery task for execution
    return {"id": command.id, "status": "queued"}


@router.get("", response_model=List[CommandListResponse])
async def list_commands(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    provider: str = Query(None),
    status: str = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0),
):
    """List user commands with optional filters."""
    query = select(Command).where(Command.user_id == current_user["user_id"])

    if provider:
        query = query.where(Command.selected_provider == provider)
    if status:
        query = query.where(Command.status == status)

    query = query.order_by(Command.created_at.desc()).limit(limit).offset(offset)

    result = await db.execute(query)
    commands = result.scalars().all()
    return commands


@router.get("/{command_id}", response_model=CommandResponse)
async def get_command(
    command_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific command with its runs."""
    result = await db.execute(
        select(Command).where(
            (Command.id == command_id) & (Command.user_id == current_user["user_id"])
        )
    )
    command = result.scalar_one_or_none()

    if not command:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Command not found")

    return command


@router.post("/{command_id}/retry", response_model=dict)
async def retry_command(
    command_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retry a failed command."""
    result = await db.execute(
        select(Command).where(
            (Command.id == command_id) & (Command.user_id == current_user["user_id"])
        )
    )
    command = result.scalar_one_or_none()

    if not command:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Command not found")

    if command.status not in ["failed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Can only retry failed commands"
        )

    command.status = "queued"
    await db.commit()

    # TODO: Trigger Celery task for execution
    return {"id": command.id, "status": "queued"}
