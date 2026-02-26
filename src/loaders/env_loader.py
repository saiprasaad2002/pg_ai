from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class MCPSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str
    mcp_server_host: str
    mcp_server_port: int
    mcp_server_transport: str

@lru_cache
def get_mcp_settings():
    settings = MCPSettings()
    return settings