from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings

class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            pool_pre_ping=True,
            pool_recycle=1800,
            pool_size=5,
            max_overflow=10,
            connect_args={
                "timeout": 10,
                "command_timeout": 30,
                "server_settings": {
                    "application_name": "qlsocket_api",
                },
            },
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.echo
)