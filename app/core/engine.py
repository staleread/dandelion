from sqlalchemy import create_engine
from .config import Settings


engine = create_engine(Settings().db_url)  # type: ignore
