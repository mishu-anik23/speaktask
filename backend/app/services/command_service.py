from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import Command, CommandRun, ProviderAccount, ExecutionLog
from app.providers.factory import ProviderFactory
from app.core.config import get_settings
from cryptography.fernet import Cipher
from datetime import datetime
import json

settings = get_settings()
cipher = Cipher(settings.fernet_secret.encode())


class CommandService:
    """Service for routing and executing commands."""

    @staticmethod
    async def get_provider_adapter(db: AsyncSession, user_id: int, provider_name: str):
        """Retrieve and decrypt provider credentials."""
        result = await db.execute(
            select(ProviderAccount).where(
                (ProviderAccount.user_id == user_id)
                & (ProviderAccount.provider_name == provider_name)
            )
        )
        account = result.scalar_one_or_none()

        if not account:
            raise Exception(f"Provider {provider_name} not connected")

        from cryptography.fernet import Fernet
        cipher = Fernet(settings.fernet_secret.encode())
        decrypted = cipher.decrypt(account.encrypted_credentials.encode()).decode()
        credentials = json.loads(decrypted)

        api_key = credentials.get("api_key")
        if not api_key:
            raise Exception("No API key found for provider")

        return ProviderFactory.create(provider_name, api_key)

    @staticmethod
    async def execute_command(db: AsyncSession, command_id: int):
        """Execute a command using the selected provider."""
        # Fetch command
        result = await db.execute(select(Command).where(Command.id == command_id))
        command = result.scalar_one_or_none()

        if not command:
            raise Exception(f"Command {command_id} not found")

        # Create command run
        run = CommandRun(command_id=command_id, started_at=datetime.utcnow())
        db.add(run)
        await db.commit()
        await db.refresh(run)

        try:
            # Get provider adapter
            adapter = await CommandService.get_provider_adapter(
                db, command.user_id, command.selected_provider
            )

            # Get prompt
            prompt = command.transcript_text or command.raw_input

            # Execute
            result_dict = await adapter.execute(prompt)

            # Update run
            run.completed_at = datetime.utcnow()
            run.result_text = result_dict["result"]
            run.tokens_used = result_dict.get("tokens_used", 0)

            # Update command
            command.status = "succeeded"

            # Log
            log = ExecutionLog(
                command_id=command_id,
                command_run_id=run.id,
                log_type="info",
                message="Command executed successfully",
            )
            db.add(log)

        except Exception as e:
            run.completed_at = datetime.utcnow()
            run.error_message = str(e)
            command.status = "failed"

            log = ExecutionLog(
                command_id=command_id,
                command_run_id=run.id,
                log_type="error",
                message=str(e),
            )
            db.add(log)

        await db.commit()
        return run
