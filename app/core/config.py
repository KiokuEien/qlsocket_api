from pathlib import Path
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class DbSettings(BaseModel):
    postgres_dsn_url: PostgresDsn = 'postgresql+asyncpg://user:password@localhost:5432/database'
    echo: bool = False

    @property
    def url(self) -> str:
        return str(self.postgres_dsn_url)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_nested_delimiter='__',
    )

    db: DbSettings = DbSettings()

    api_v1_prefix: str = '/api/v1'

settings = Settings()
