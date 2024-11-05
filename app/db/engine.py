from sqlalchemy.ext.asyncio import create_async_engine
from app.config import Settings

engine = create_async_engine(
    Settings().db_url,  # type: ignore
    echo=True,
    future=True,
)
