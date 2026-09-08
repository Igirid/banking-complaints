import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DEFAULT_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./banking_complaints.db")


def _create_engine(url: str):
    return create_engine(url, pool_pre_ping=True, future=True)


try:
    engine = _create_engine(DEFAULT_DATABASE_URL)
except Exception:
    fallback_url = os.getenv("DATABASE_URL_FALLBACK", "sqlite:///./banking_complaints.db")
    if fallback_url == DEFAULT_DATABASE_URL:
        raise
    engine = create_engine(
        fallback_url,
        connect_args={"check_same_thread": False},
        future=True,
    )

DATABASE_URL = str(engine.url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
