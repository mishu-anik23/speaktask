from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.core.security import get_current_user
from app.core.config import get_settings
from app.models.models import ProviderAccount, AuditLog
from app.schemas.schemas import ProviderAccountResponse, ProviderAccountCreate
from cryptography.fernet import Fernet
from datetime import datetime
from typing import List
import json

router = APIRouter(prefix="/providers", tags=["providers"])

settings = get_settings()
cipher = Fernet(settings.fernet_secret.encode())


@router.get("", response_model=List[dict])
async def list_providers(current_user: dict = Depends(get_current_user)):
    """List available providers and their status."""
    providers = ["openai", "claude", "gemini"]
    return [{"name": p, "connected": False} for p in providers]


@router.post("/connect")
async def connect_provider(
    data: ProviderAccountCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Save encrypted API key for a provider."""
    # Encrypt credentials
    credentials_json = json.dumps(data.credentials).encode()
    encrypted = cipher.encrypt(credentials_json).decode()

    # Check if provider already exists
    result = await db.execute(
        select(ProviderAccount).where(
            (ProviderAccount.user_id == current_user["user_id"])
            & (ProviderAccount.provider_name == data.provider_name)
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        existing.encrypted_credentials = encrypted
        existing.status = "active"
    else:
        account = ProviderAccount(
            user_id=current_user["user_id"],
            provider_name=data.provider_name,
            encrypted_credentials=encrypted,
            status="active",
        )
        db.add(account)

    # Audit log
    audit = AuditLog(
        user_id=current_user["user_id"],
        action_type="provider_connected",
        resource_type="provider",
        resource_id=None,
        metadata=json.dumps({"provider": data.provider_name}),
    )
    db.add(audit)

    await db.commit()
    return {"status": "connected", "provider": data.provider_name}


@router.post("/disconnect")
async def disconnect_provider(
    provider_name: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Remove provider credentials."""
    result = await db.execute(
        select(ProviderAccount).where(
            (ProviderAccount.user_id == current_user["user_id"])
            & (ProviderAccount.provider_name == provider_name)
        )
    )
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not connected")

    await db.delete(account)

    # Audit log
    audit = AuditLog(
        user_id=current_user["user_id"],
        action_type="provider_disconnected",
        resource_type="provider",
        metadata=json.dumps({"provider": provider_name}),
    )
    db.add(audit)

    await db.commit()
    return {"status": "disconnected", "provider": provider_name}


@router.get("/status")
async def check_provider_status(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Check which providers are connected."""
    result = await db.execute(
        select(ProviderAccount).where(ProviderAccount.user_id == current_user["user_id"])
    )
    accounts = result.scalars().all()
    connected = {acc.provider_name: acc.status == "active" for acc in accounts}

    return {
        "openai": connected.get("openai", False),
        "claude": connected.get("claude", False),
        "gemini": connected.get("gemini", False),
    }
