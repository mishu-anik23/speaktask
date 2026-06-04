from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.models import Setting
from app.schemas.schemas import SettingResponse, SettingUpdate
from typing import List

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=List[SettingResponse])
async def get_settings(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user settings."""
    result = await db.execute(select(Setting).where(Setting.user_id == current_user["user_id"]))
    settings = result.scalars().all()
    return settings


@router.patch("")
async def update_settings(
    data: SettingUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update user settings."""
    result = await db.execute(
        select(Setting).where(
            (Setting.user_id == current_user["user_id"]) & (Setting.key == data.key)
        )
    )
    setting = result.scalar_one_or_none()

    if setting:
        setting.value = data.value
    else:
        setting = Setting(user_id=current_user["user_id"], key=data.key, value=data.value)
        db.add(setting)

    await db.commit()
    await db.refresh(setting)
    return setting
