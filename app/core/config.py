from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class DbSettings(BaseModel):
    url: str = 'postgresql+asyncpg://user:password@localhost:5432/database'
    echo: bool = False

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__'
    )

    db: DbSettings = DbSettings()

    api_v1_prefix: str = '/api/v1'

settings = Settings()