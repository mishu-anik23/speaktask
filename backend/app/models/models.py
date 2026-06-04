from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Enum, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    provider_accounts = relationship("ProviderAccount", back_populates="user", cascade="all, delete-orphan")
    commands = relationship("Command", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("Setting", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")


class ProviderAccount(Base):
    __tablename__ = "provider_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    provider_name = Column(String(50))  # 'openai', 'claude', 'gemini'
    encrypted_credentials = Column(Text)
    status = Column(String(20), default="active")  # 'active', 'expired', 'inactive'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="provider_accounts")


class CommandStatus(str, enum.Enum):
    processing = "processing"
    succeeded = "succeeded"
    failed = "failed"
    queued = "queued"


class Command(Base):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    input_type = Column(String(20))  # 'voice', 'text'
    raw_input = Column(Text)
    transcript_text = Column(Text, nullable=True)
    selected_provider = Column(String(50))  # 'openai', 'claude', 'gemini'
    command_intent = Column(String(255), nullable=True)
    status = Column(String(20), default="processing")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (Index("idx_user_created", "user_id", "created_at"),)

    user = relationship("User", back_populates="commands")
    runs = relationship("CommandRun", back_populates="command", cascade="all, delete-orphan")
    transcripts = relationship("Transcript", back_populates="command", cascade="all, delete-orphan")
    execution_logs = relationship("ExecutionLog", back_populates="command", cascade="all, delete-orphan")


class CommandRun(Base):
    __tablename__ = "command_runs"

    id = Column(Integer, primary_key=True, index=True)
    command_id = Column(Integer, ForeignKey("commands.id", ondelete="CASCADE"))
    started_at = Column(DateTime)
    completed_at = Column(DateTime, nullable=True)
    result_text = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    cost_estimate = Column(String(50), nullable=True)

    command = relationship("Command", back_populates="runs")
    execution_logs = relationship("ExecutionLog", back_populates="run", cascade="all, delete-orphan")


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, index=True)
    command_id = Column(Integer, ForeignKey("commands.id", ondelete="CASCADE"))
    raw_audio_url = Column(String(500), nullable=True)
    transcript_text = Column(Text)
    confidence = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    command = relationship("Command", back_populates="transcripts")


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id = Column(Integer, primary_key=True, index=True)
    command_id = Column(Integer, ForeignKey("commands.id", ondelete="CASCADE"))
    command_run_id = Column(Integer, ForeignKey("command_runs.id", ondelete="CASCADE"), nullable=True)
    log_type = Column(String(50))  # 'info', 'error', 'debug'
    message = Column(Text)
    metadata = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    command = relationship("Command", back_populates="execution_logs")
    run = relationship("CommandRun", back_populates="execution_logs")


class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    key = Column(String(100))
    value = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="settings")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    action_type = Column(String(50))
    resource_type = Column(String(50))
    resource_id = Column(Integer, nullable=True)
    metadata = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="audit_logs")
