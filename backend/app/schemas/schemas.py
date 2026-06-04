from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# Auth Schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Provider Schemas
class ProviderAccountCreate(BaseModel):
    provider_name: str
    credentials: dict


class ProviderAccountResponse(BaseModel):
    id: int
    provider_name: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# Command Schemas
class CommandCreate(BaseModel):
    input_type: str  # 'voice', 'text'
    raw_input: str
    transcript_text: Optional[str] = None
    selected_provider: Optional[str] = None


class CommandRunResponse(BaseModel):
    id: int
    started_at: datetime
    completed_at: Optional[datetime]
    result_text: Optional[str]
    error_message: Optional[str]
    tokens_used: Optional[int]
    cost_estimate: Optional[str]

    class Config:
        from_attributes = True


class CommandResponse(BaseModel):
    id: int
    input_type: str
    raw_input: str
    transcript_text: Optional[str]
    selected_provider: str
    status: str
    created_at: datetime
    runs: List[CommandRunResponse] = []

    class Config:
        from_attributes = True


class CommandListResponse(BaseModel):
    id: int
    input_type: str
    raw_input: str
    status: str
    selected_provider: str
    created_at: datetime

    class Config:
        from_attributes = True


# Settings Schemas
class SettingUpdate(BaseModel):
    key: str
    value: str


class SettingResponse(BaseModel):
    id: int
    key: str
    value: str
    updated_at: datetime

    class Config:
        from_attributes = True
