import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str | None = None
    PORT: int = int(os.getenv("AIDE_AGENT_PORT", 8123))
    SOCKET_PATH: str | None = os.getenv("AIDE_AGENT_SOCKET", None)
    ALLOW_REMOTE: bool = os.getenv("AIDE_AGENT_ALLOW_REMOTE", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    SENSITIVE_PATHS: list[str] = ["/etc/shadow", "/root/.ssh", "~/.ssh"]

    class Config:
        env_file = ".env"

settings = Settings()