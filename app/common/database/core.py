from sqlalchemy import create_engine
from app.config import Settings


engine = create_engine(Settings().db_url)  # type: ignore
