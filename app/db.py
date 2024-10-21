import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from .config import settings

engine = create_async_engine(
  settings.db_url,
  echo=True,
  future=True,
)
