from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.models import Command, Transcript
from app.schemas.schemas import CommandResponse
from datetime import datetime
import aiofiles
import os

router = APIRouter(prefix="/voice", tags=["voice"])

UPLOAD_DIR = "uploads/audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/submit")
async def submit_voice(
    file: UploadFile = File(...),
    selected_provider: str = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Accept audio file and create a command."""
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")

    # Save audio file
    file_path = f"{UPLOAD_DIR}/{current_user['user_id']}_{datetime.utcnow().timestamp()}.wav"
    try:
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    # Create command record
    command = Command(
        user_id=current_user["user_id"],
        input_type="voice",
        raw_input=file_path,
        status="processing",
        selected_provider=selected_provider or "openai",
    )
    db.add(command)
    await db.commit()
    await db.refresh(command)

    return {"command_id": command.id, "status": "processing"}


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Transcribe audio to text."""
    # For now, just return a placeholder
    # In production, call Whisper API
    return {"transcript_text": "Sample transcription"}
